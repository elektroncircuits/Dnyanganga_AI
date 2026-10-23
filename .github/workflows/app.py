
import os
import sqlite3
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai

# ---------------- CONFIGURATION ----------------

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "gyangangaa.db"

load_dotenv(BASE_DIR / ".env")

st.set_page_config(
    page_title="ज्ञानगंगा AI",
    page_icon="📚",
    layout="wide",
)

TOPICS = [
    "Embedded C",
    "ARM Cortex-M",
    "STM32",
    "ESP32",
    "RTOS",
    "FPGA",
    "PCB Design",
    "Digital Electronics",
    "Electronics Fundamentals",
    "Processor Architecture",
    "Embedded Linux",
]

# ---------------- DATABASE ----------------

def get_connection():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                resource_type TEXT NOT NULL,
                topic TEXT NOT NULL,
                level TEXT NOT NULL,
                description TEXT,
                url TEXT NOT NULL,
                source TEXT NOT NULL
            )
        """)

        existing = conn.execute(
            "SELECT COUNT(*) FROM resources"
        ).fetchone()[0]

        if existing == 0:
            starter_resources = [
                (
                    "All About Circuits Textbook",
                    "Book / Reference",
                    "Electronics Fundamentals",
                    "Beginner",
                    "Free online electronics textbook.",
                    "https://www.allaboutcircuits.com/textbook/",
                    "All About Circuits",
                ),
                (
                    "GNU C Documentation",
                    "Documentation",
                    "Embedded C",
                    "Intermediate",
                    "C compiler documentation and reference.",
                    "https://gcc.gnu.org/onlinedocs/",
                    "GNU",
                ),
                (
                    "Arm Developer Training",
                    "Course",
                    "ARM Cortex-M",
                    "Beginner",
                    "Official Arm learning resources.",
                    "https://developer.arm.com/Training",
                    "Arm",
                ),
                (
                    "STM32 Education",
                    "Course",
                    "STM32",
                    "Beginner",
                    "Official STM32 training resources.",
                    "https://www.st.com/content/st_com/en/support/learning/stm32-education.html",
                    "STMicroelectronics",
                ),
                (
                    "ESP-IDF Programming Guide",
                    "Documentation",
                    "ESP32",
                    "Intermediate",
                    "Official ESP32 development framework documentation.",
                    "https://docs.espressif.com/projects/esp-idf/en/stable/esp32/",
                    "Espressif",
                ),
                (
                    "FreeRTOS Documentation",
                    "Documentation",
                    "RTOS",
                    "Intermediate",
                    "RTOS concepts, APIs, and guides.",
                    "https://www.freertos.org/Documentation/RTOS_book.html",
                    "FreeRTOS",
                ),
                (
                    "Nandland Tutorials",
                    "Video / Tutorial",
                    "FPGA",
                    "Beginner",
                    "FPGA and digital logic learning material.",
                    "https://nandland.com/",
                    "Nandland",
                ),
                (
                    "KiCad Documentation",
                    "Course / Tutorial",
                    "PCB Design",
                    "Beginner",
                    "Learn PCB design using KiCad.",
                    "https://docs.kicad.org/",
                    "KiCad",
                ),
                (
                    "NPTEL Courses",
                    "Course / Video",
                    "Digital Electronics",
                    "Beginner",
                    "University courses and video lectures.",
                    "https://nptel.ac.in/",
                    "NPTEL",
                ),
                (
                    "Linux Kernel Documentation",
                    "Documentation",
                    "Embedded Linux",
                    "Advanced",
                    "Official Linux kernel documentation.",
                    "https://docs.kernel.org/",
                    "Linux",
                ),
                (
                    "MIT OpenCourseWare",
                    "Course / Video",
                    "Processor Architecture",
                    "Intermediate",
                    "Open university course materials.",
                    "https://ocw.mit.edu/",
                    "MIT",
                ),
            ]

            conn.executemany("""
                INSERT INTO resources
                (title, resource_type, topic, level,
                 description, url, source)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, starter_resources)


initialize_database()


def load_resources():
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM resources ORDER BY topic, title"
        ).fetchall()


# ---------------- SIDEBAR ----------------

st.sidebar.title("📚 ज्ञानगंगा AI")
st.sidebar.caption("Electronics Learning Portal")

page = st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "Courses & Videos",
        "Books & References",
        "AI Study Assistant",
        "Add Resource",
    ],
)

st.sidebar.divider()
st.sidebar.write("Created by Ishan Kulkarni")

# ---------------- HOME ----------------

if page == "Home":
    st.title("ज्ञानगंगा AI")
    st.subheader(
        "Learn electronics. Build embedded systems. "
        "Grow your skills."
    )

    st.write(
        "Your learning hub for electronics, embedded "
        "software, courses, videos, and reference material."
    )

    resources = load_resources()

    course_count = sum(
        "course" in r["resource_type"].lower()
        or "video" in r["resource_type"].lower()
        or "tutorial" in r["resource_type"].lower()
        for r in resources
    )

    book_count = sum(
        "book" in r["resource_type"].lower()
        or "reference" in r["resource_type"].lower()
        for r in resources
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Total resources", len(resources))
    c2.metric("Courses and videos", course_count)
    c3.metric("Books and references", book_count)

    st.markdown("### Learning tracks")
    cols = st.columns(3)

    for i, topic in enumerate(TOPICS):
        cols[i % 3].markdown(f"- {topic}")

    st.info(
        "Use official or open educational links. "
        "Some courses may charge for certificates."
    )

# ---------------- RESOURCE LIBRARY ----------------

elif page in ("Courses & Videos", "Books & References"):
    st.title(page)

    search = st.text_input("Search resources")
    selected_topic = st.selectbox(
        "Topic", ["All topics"] + TOPICS
    )
    selected_level = st.selectbox(
        "Level",
        ["All levels", "Beginner", "Intermediate", "Advanced"],
    )

    resources = load_resources()

    for r in resources:
        kind = r["resource_type"].lower()

        if page == "Courses & Videos":
            if not any(
                word in kind
                for word in ("course", "video", "tutorial")
            ):
                continue
        else:
            if not any(
                word in kind for word in ("book", "reference")
            ):
                continue

        if (
            selected_topic != "All topics"
            and r["topic"] != selected_topic
        ):
            continue

        if (
            selected_level != "All levels"
            and r["level"] != selected_level
        ):
            continue

        search_text = " ".join(
            str(r[key] or "")
            for key in (
                "title", "topic", "description", "source"
            )
        ).lower()

        if search and search.lower() not in search_text:
            continue

        with st.container(border=True):
            st.markdown(f"### {r['title']}")
            st.caption(
                f"{r['topic']} | {r['level']} | "
                f"{r['resource_type']} | {r['source']}"
            )
            st.write(r["description"])
            st.markdown(f"[Open resource]({r['url']})")

# ---------------- GEMINI STUDY ASSISTANT ----------------

elif page == "AI Study Assistant":
    st.title("AI Study Assistant")
    st.write(
        "Ask about Embedded C, microcontrollers, RTOS, "
        "digital electronics, or your study plan."
    )

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    if not api_key:
        st.warning(
            "Gemini is not configured. Add your API key "
            "to the .env file to enable AI chat."
        )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask an electronics question...")

    if prompt:
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        answer = ""

        if api_key:
            try:
                client = genai.Client(api_key=api_key)

                history = []
                for item in st.session_state.messages[:-1]:
                    role = (
                        "user"
                        if item["role"] == "user"
                        else "model"
                    )
                    history.append({
                        "role": role,
                        "parts": [{"text": item["content"]}],
                    })

                chat = client.chats.create(
                    model=model,
                    history=history,
                    config={
                        "system_instruction": (
                            "You are ज्ञानगंगा AI, a friendly "
                            "electronics engineering tutor. "
                            "Explain concepts step by step, "
                            "give practical examples, and help "
                            "students debug code safely. Be honest "
                            "about uncertainty. Do not claim "
                            "copyrighted books are freely available."
                        )
                    },
                )

                response = chat.send_message(prompt)
                answer = response.text or "Please try asking again."

            except Exception as exc:
                answer = (
                    f"Gemini error: {exc}\n\n"
                    "Check your API key, model availability, "
                    "internet connection, and API quota."
                )
        else:
            answer = (
                "Add a valid GEMINI_API_KEY to your .env file "
                "and restart the app to enable AI responses."
            )

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

# ---------------- ADD A RESOURCE ----------------

elif page == "Add Resource":
    st.title("Add a Learning Resource")

    with st.form("resource_form", clear_on_submit=True):
        title = st.text_input("Resource title")

        resource_type = st.selectbox(
            "Resource type",
            [
                "Course",
                "Video / Tutorial",
                "Book / Reference",
                "Documentation",
                "Other",
            ],
        )

        topic = st.selectbox("Topic", TOPICS)
        level = st.selectbox(
            "Level", ["Beginner", "Intermediate", "Advanced"]
        )
        description = st.text_area("Description")
        url = st.text_input("Resource URL")
        source = st.text_input("Publisher or source")

        submitted = st.form_submit_button("Save resource")

    if submitted:
        if (
            not title.strip()
            or not url.strip().startswith(("https://", "http://"))
            or not source.strip()
        ):
            st.error(
                "Enter a title, valid HTTP/HTTPS URL, and source."
            )
        else:
            with get_connection() as conn:
                conn.execute("""
                    INSERT INTO resources
                    (title, resource_type, topic, level,
                     description, url, source)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    title.strip(),
                    resource_type,
                    topic,
                    level,
                    description.strip(),
                    url.strip(),
                    source.strip(),
                ))

            st.success("Resource saved successfully.")
            st.rerun()

st.divider()
st.caption(
    "ज्ञानगंगा AI | Created by Ishan Kulkarni"
)
