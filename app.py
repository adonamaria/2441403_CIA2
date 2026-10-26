"""
AI Quiz Arena  --  DSC401-6 Artificial Intelligence (Units I & II)
Interactive quiz game built with Streamlit.

Run locally :  streamlit run app.py
"""
import csv
import io
import json
import random
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

from questions import (QUESTIONS, TOPICS, TOPIC_SHORT, LEVEL_POINTS, input_mode, check_text,
                       correct_text, time_limit)

st.set_page_config(page_title="AI Quiz Arena | DSC401-6", page_icon="🧠", layout="centered")

QBY = {q["id"]: q for q in QUESTIONS}
LB_FILE = Path(__file__).with_name("leaderboard.json")
LEVEL_ICON = {"Easy": "🟢", "Medium": "🟡", "Hard": "🔴"}
LETTERS = "ABCDEFGH"
LIFELINES0 = {"fifty": 2, "hint": 3, "skip": 1, "time": 1}
HINT_PENALTY, FIFTY_PENALTY, EXTRA_SECONDS = 0.25, 0.25, 20

st.markdown(
    """
    <style>
      .badge{display:inline-block;padding:2px 10px;border-radius:12px;font-size:0.78rem;margin-right:6px;
             background:rgba(120,120,160,.18);}
      .big{font-size:2.4rem;font-weight:700;line-height:1.1}
      div[data-testid="stMetricValue"]{font-size:1.6rem}
    </style>
    """,
    unsafe_allow_html=True,
)

ss = st.session_state


def md(text):
    """Escape the '*' of 'A*' so Streamlit's Markdown does not read it as italics."""
    return str(text).replace("A*", "A\\*")


# ----------------------------------------------------------------------------- leaderboard
def load_lb():
    try:
        return json.loads(LB_FILE.read_text())
    except Exception:
        return []


def save_lb(entry):
    rows = load_lb()
    rows.append(entry)
    rows.sort(key=lambda r: (-r["score"], -r["pct"], r["secs"]))
    try:
        LB_FILE.write_text(json.dumps(rows[:100], indent=1))
    except Exception:
        pass  # read-only file system: the in-session result still works


def lb_frame(n=10):
    rows = load_lb()[:n]
    if not rows:
        return None
    df = pd.DataFrame(rows)
    df.insert(0, "Rank", range(1, len(df) + 1))
    df["Score"] = df.apply(lambda r: f"{r['score']:g} / {r['max']:g}", axis=1)
    df["Time"] = df["secs"].apply(lambda s: f"{int(s // 60)}m {int(s % 60):02d}s")
    return df[["Rank", "name", "Score", "pct", "level", "n", "Time"]].rename(
        columns={"name": "Player", "pct": "%", "level": "Level", "n": "Qs"})


# ----------------------------------------------------------------------------- state helpers
def fresh_qstate(qid):
    q = QBY[qid]
    limit = time_limit(q)
    return dict(start=time.time(), limit=limit, deadline=time.time() + limit, hint=False,
                fifty=None, submitted=False, outcome=None, gained=0.0, feedback="")


def start_quiz(name, level, n, topics, timer_on):
    pool = [q for q in QUESTIONS if (level == "Mixed" or q["level"] == level) and q["topic"] in topics]
    random.shuffle(pool)
    chosen = pool[:n]
    items = []
    for q in chosen:
        mode = input_mode(q)
        size = len(q["options"]) if mode == "choice" else len(q["right"]) if mode == "match" else 0
        order = list(range(size))
        if q["type"] in ("MCQ", "Scenario", "Problem Solving", "Match the Following"):
            random.shuffle(order)  # True/False and Assertion-Reason keep their fixed order
        items.append(dict(qid=q["id"], order=order))
    ss.update(stage="quiz", name=(name.strip() or "Anonymous"), level=level, qitems=items,
              timer_on=timer_on, qi=0, results=[], score=0.0, streak=0, best_streak=0,
              life=dict(LIFELINES0), t0=time.time(), saved=False, run=ss.get("run", 0) + 1)
    ss.qs = fresh_qstate(items[0]["qid"])


def finalize(frac, outcome, user_text, gained):
    """Record the result of the current question."""
    q = QBY[ss.qitems[ss.qi]["qid"]]
    qs = ss.qs
    qs.update(submitted=True, outcome=outcome, gained=gained)
    full = outcome == "correct"
    ss.streak = ss.streak + 1 if full else 0
    ss.best_streak = max(ss.best_streak, ss.streak)
    ss.score += gained
    ss.results.append(dict(
        id=q["id"], topic=q["topic"], type=q["type"], level=q["level"], outcome=outcome,
        base=LEVEL_POINTS[q["level"]], gained=gained, user=user_text,
        used_hint=qs["hint"], used_fifty=qs["fifty"] is not None,
        secs=round(time.time() - qs["start"], 1)))


def advance():
    ss.qi += 1
    if ss.qi >= len(ss.qitems):
        ss.stage = "result"
    else:
        ss.qs = fresh_qstate(ss.qitems[ss.qi]["qid"])


def widget_key(*parts):
    return "_".join(["w", str(ss.run), str(ss.qi), *map(str, parts)])


def read_answer(q, item):
    """Return (fraction_correct, printable_answer) or None if nothing was answered."""
    mode = input_mode(q)
    if mode == "choice":
        pos = ss.get(widget_key("c"))
        if pos is None:
            return None
        return (1.0 if item["order"][pos] == q["ans"] else 0.0), q["options"][item["order"][pos]]
    if mode == "text":
        txt = (ss.get(widget_key("t")) or "").strip()
        if not txt:
            return None
        return (1.0 if check_text(q, txt) else 0.0), txt
    picks = [ss.get(widget_key("m", i)) for i in range(len(q["left"]))]
    if any(p is None for p in picks):
        return None
    ok = sum(item["order"][LETTERS.index(p)] == q["ans"][i] for i, p in enumerate(picks))
    text = "; ".join(f"{q['left'][i]} → {p}" for i, p in enumerate(picks))
    return ok / len(q["left"]), text


# ----------------------------------------------------------------------------- callbacks
def cb_submit():
    q = QBY[ss.qitems[ss.qi]["qid"]]
    ans = read_answer(q, ss.qitems[ss.qi])
    if ans is None:
        ss.warn = True
        return
    ss.warn = False
    frac, text = ans
    qs = ss.qs
    mult = 1 - HINT_PENALTY * qs["hint"] - FIFTY_PENALTY * (qs["fifty"] is not None)
    gained = round(LEVEL_POINTS[q["level"]] * frac * mult, 2)
    outcome = "correct" if frac == 1 else "partial" if frac > 0 else "wrong"
    finalize(frac, outcome, text, gained)


def cb_timeout():
    if not ss.qs["submitted"]:
        finalize(0.0, "timeout", "(no answer – time up)", 0.0)


def cb_fifty():
    q, item = QBY[ss.qitems[ss.qi]["qid"]], ss.qitems[ss.qi]
    wrong = [p for p in range(len(item["order"])) if item["order"][p] != q["ans"]]
    ss.qs["fifty"] = random.sample(wrong, 2)
    ss.life["fifty"] -= 1


def cb_hint():
    ss.qs["hint"] = True
    ss.life["hint"] -= 1


def cb_time():
    ss.qs["deadline"] += EXTRA_SECONDS
    ss.qs["limit"] += EXTRA_SECONDS
    ss.life["time"] -= 1


def cb_skip():
    finalize(0.0, "skipped", "(skipped)", 0.0)
    advance()


def cb_next():
    advance()


def cb_restart():
    for k in ("stage", "qitems", "results"):
        ss.pop(k, None)
    ss.stage = "home"


# ----------------------------------------------------------------------------- timer
@st.fragment(run_every=1)
def timer_box():
    qs = ss.qs
    if not ss.timer_on:
        st.caption("⏱ Timer is off for this game")
        return
    if qs["submitted"]:
        return
    remaining = int(round(qs["deadline"] - time.time()))
    frac = max(0.0, min(1.0, remaining / qs["limit"]))
    icon = "⏱" if remaining > 10 else "🔥"
    st.progress(frac, text=f"{icon} {max(remaining, 0)} s left")
    if remaining <= 0:
        cb_timeout()
        st.rerun()


# ----------------------------------------------------------------------------- HOME
def page_home():
    st.title("🧠 AI Quiz Arena")
    st.markdown("**DSC401-6 Artificial Intelligence · Units I & II**  \n"
                "Agents, search, heuristics, hill climbing, CSP and means-end analysis, in a game.")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        name = c1.text_input("Your name", value=ss.get("name", ""), placeholder="e.g. Arnold")
        level = c2.selectbox("Difficulty level", ["Mixed", "Easy", "Medium", "Hard"],
                             help="Easy = 1 pt, Medium = 2 pts, Hard = 3 pts per question.")
        topics = st.multiselect("Topics", TOPICS, default=TOPICS)
        pool = [q for q in QUESTIONS if (level == "Mixed" or q["level"] == level) and q["topic"] in topics]
        if len(pool) == 0:
            st.warning("No questions match this selection.")
            n = 0
        elif len(pool) <= 5:
            n = len(pool)
            st.caption(f"{n} questions available.")
        else:
            n = st.slider("Number of questions", 5, len(pool), min(20, len(pool)))
        timer_on = st.toggle("⏱ Timer (per question)", value=True)
        st.button("🚀 Start the quiz", type="primary", width="stretch", disabled=n == 0,
                  on_click=lambda: start_quiz(name, level, n, topics, timer_on))
    with st.expander("How the game works", expanded=True):
        st.markdown(
            """
- **Random questions:** every game draws a fresh random set from the 60-question bank, with options shuffled.
- **Formats:** MCQ, True/False, Assertion-Reason, Fill in the Blank, Match the Following, real-world
  Scenarios and search / state-space Problem Solving.
- **Scoring:** Easy 1 pt · Medium 2 pts · Hard 3 pts. Match questions give partial credit. No negative marking.
- **Lifelines:** 🎯 50:50 ×2 (−25% of the question's points) · 💡 Hint ×3 (−25%) ·
  ⏭ Skip ×1 · ⏳ +20 s ×1.
- **Immediate feedback:** after each answer you see the correct answer and an explanation.
- **At the end:** score, topic-wise analysis, full review with viva follow-up questions, and the leaderboard.
            """
        )


# ----------------------------------------------------------------------------- QUIZ
def render_question(q, item):
    qs = ss.qs
    locked = qs["submitted"]
    mode = input_mode(q)
    st.markdown(
        f"<span class='badge'>{LEVEL_ICON[q['level']]} {q['level']} · {LEVEL_POINTS[q['level']]} pt</span>"
        f"<span class='badge'>{q['type']}</span><span class='badge'>{q['topic']}</span>",
        unsafe_allow_html=True)
    st.markdown(f"##### {md(q['q'])}" if "\n" not in q["q"] else md(q["q"]))
    if q.get("code"):
        st.code(q["code"], language=None)
    if qs["hint"]:
        st.info(f"💡 **Hint:** {md(q['hint'])}")

    if mode == "choice":
        shown = [p for p in range(len(item["order"])) if not (qs["fifty"] and p in qs["fifty"])]
        st.radio("Choose one answer", shown, index=None, disabled=locked, key=widget_key("c"),
                 format_func=lambda p: f"{LETTERS[p]}.  {md(q['options'][item['order'][p]])}")
    elif mode == "text":
        hint = "Type a number" if q["kind"] == "num" else "Type your answer"
        st.text_input("Your answer", disabled=locked, key=widget_key("t"), placeholder=hint)
    else:
        for p, o in enumerate(item["order"]):
            st.markdown(f"**{LETTERS[p]}.** {md(q['right'][o])}")
        st.write("")
        for i, left in enumerate(q["left"]):
            st.selectbox(f"**{i + 1}. {md(left)}**", list(LETTERS[:len(item['order'])]), index=None,
                         placeholder="Pick a letter…", disabled=locked, key=widget_key("m", i))


def page_quiz():
    q = QBY[ss.qitems[ss.qi]["qid"]]
    item, qs, life = ss.qitems[ss.qi], ss.qs, ss.life
    n = len(ss.qitems)

    top = st.columns([3, 1, 1])
    top[0].progress(ss.qi / n, text=f"Question {ss.qi + 1} of {n}")
    top[1].metric("Score", f"{ss.score:g}")
    top[2].metric("Streak", f"🔥 {ss.streak}")

    timer_box()

    mode = input_mode(q)
    done = qs["submitted"]
    lc = st.columns(4)
    lc[0].button(f"🎯 50:50 ({life['fifty']})", on_click=cb_fifty, width="stretch",
                 disabled=done or life["fifty"] == 0 or mode != "choice" or len(item["order"]) < 4
                 or qs["fifty"] is not None,
                 help="Removes two wrong options (not available for True/False, text or match).")
    lc[1].button(f"💡 Hint ({life['hint']})", on_click=cb_hint, width="stretch",
                 disabled=done or life["hint"] == 0 or qs["hint"])
    lc[2].button(f"⏭ Skip ({life['skip']})", on_click=cb_skip, width="stretch",
                 disabled=done or life["skip"] == 0)
    lc[3].button(f"⏳ +{EXTRA_SECONDS}s ({life['time']})", on_click=cb_time, width="stretch",
                 disabled=done or life["time"] == 0 or not ss.timer_on)

    with st.container(border=True):
        render_question(q, item)

    if not done:
        st.button("✅ Submit answer", type="primary", on_click=cb_submit, width="stretch")
        if ss.get("warn"):
            st.warning("Please answer first (or use Skip).")
            ss.warn = False
        return

    # ---- immediate feedback
    o = qs["outcome"]
    if o == "correct":
        st.success(f"✅ Correct! +{qs['gained']:g} point(s)")
    elif o == "partial":
        st.warning(f"🟡 Partly correct: +{qs['gained']:g} point(s)")
    elif o == "timeout":
        st.error("⏰ Time's up!")
    else:
        st.error("❌ Not quite.")
    if o != "correct":
        st.markdown(f"**Correct answer:** {md(correct_text(q))}")
    st.markdown(md(q["exp"]))
    last = ss.qi + 1 >= n
    st.button("🏁 Finish quiz" if last else "Next question ➜", type="primary", on_click=cb_next,
              width="stretch")


# ----------------------------------------------------------------------------- RESULT
def grade(pct):
    for cut, title in [(90, "🏆 AI Grandmaster"), (75, "🥇 Search Specialist"), (60, "🥈 Rational Agent"),
                       (40, "🥉 Hill Climber: keep climbing!")]:
        if pct >= cut:
            return title
    return "🌱 Fresh start state: try again!"


def page_result():
    res = ss.results
    max_pts = sum(r["base"] for r in res)
    pct = round(100 * ss.score / max_pts, 1) if max_pts else 0
    secs = time.time() - ss.t0
    if not ss.saved:
        save_lb(dict(name=ss.name, score=round(ss.score, 2), max=max_pts, pct=pct, level=ss.level,
                     n=len(res), secs=round(secs), date=datetime.now().strftime("%Y-%m-%d %H:%M")))
        ss.saved = True
        if pct >= 80:
            st.balloons()

    st.title("🎉 Quiz complete")
    st.markdown(f"<div class='big'>{ss.score:g} / {max_pts:g} &nbsp; ({pct}%)</div>", unsafe_allow_html=True)
    st.subheader(grade(pct))
    c = st.columns(4)
    c[0].metric("Correct", f"{sum(r['outcome'] == 'correct' for r in res)} / {len(res)}")
    c[1].metric("Best streak", f"🔥 {ss.best_streak}")
    c[2].metric("Time", f"{int(secs // 60)}m {int(secs % 60):02d}s")
    c[3].metric("Lifelines used", sum(LIFELINES0.values()) - sum(ss.life.values()))

    tab1, tab2, tab3 = st.tabs(["📊 Topic analysis", "📝 Review & viva prep", "🏆 Leaderboard"])
    with tab1:
        df = pd.DataFrame(res)
        g = df.groupby("topic").agg(earned=("gained", "sum"), possible=("base", "sum"))
        g["Score %"] = (100 * g["earned"] / g["possible"]).round(0)
        st.bar_chart(g["Score %"].rename(index=TOPIC_SHORT), horizontal=True, y_label="Score %")
        weak = g[g["Score %"] < 70].sort_values("Score %").head(3).index.tolist()
        if weak:
            st.info("Revise first: **" + "**, **".join(weak) + "**")
        else:
            st.success("Strong across every topic. Try a harder level!")
        st.dataframe(g.rename(columns={"earned": "Points earned", "possible": "Points possible"}),
                     width="stretch")
        t = df.groupby("type")["outcome"].apply(lambda s: f"{(s == 'correct').sum()} / {len(s)}")
        st.caption("Correct by question format")
        st.dataframe(t.rename("Correct"), width="stretch")
    with tab2:
        icon = {"correct": "✅", "partial": "🟡", "wrong": "❌", "timeout": "⏰", "skipped": "⏭"}
        for k, r in enumerate(res, 1):
            q = QBY[r["id"]]
            with st.expander(f"{icon[r['outcome']]}  Q{k}. [{q['type']}] {md(q['q'].splitlines()[0][:90])}"):
                st.markdown(md(q["q"]))
                if q.get("code"):
                    st.code(q["code"], language=None)
                st.markdown(f"**Your answer:** {md(r['user'])}")
                st.markdown(f"**Correct answer:** {md(correct_text(q))}")
                st.markdown(md(q["exp"]))
                st.success(f"🎓 **Be ready for the follow-up:** {md(q['follow'][0])}\n\n**Answer:** {md(q['follow'][1])}")
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["No", "QuestionID", "Topic", "Type", "Level", "Outcome", "Points", "YourAnswer", "Seconds"])
        for k, r in enumerate(res, 1):
            w.writerow([k, r["id"], r["topic"], r["type"], r["level"], r["outcome"], r["gained"], r["user"],
                        r["secs"]])
        st.download_button("⬇️ Download my result (CSV)", buf.getvalue(), "my_ai_quiz_result.csv", "text/csv")
    with tab3:
        lb = lb_frame(15)
        if lb is not None:
            st.dataframe(lb, hide_index=True, width="stretch")
    st.button("🔁 Play again", type="primary", on_click=cb_restart, width="stretch")


# ----------------------------------------------------------------------------- router
if "stage" not in ss:
    ss.stage = "home"
{"home": page_home, "quiz": page_quiz, "result": page_result}[ss.stage]()


# ----------------------------------------------------------------------------- sidebar
with st.sidebar:
    st.header("🏆 Leaderboard")
    df = lb_frame(10)
    if df is None:
        st.caption("No scores yet: be the first!")
    else:
        st.dataframe(df, hide_index=True, width="stretch")
    st.divider()
    st.caption("DSC401-6 · Artificial Intelligence\nUnits I & II quiz game · 60-question bank")
