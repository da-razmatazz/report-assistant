import streamlit as st
from azrieli_playbook import azrieli_workflow # ייבוא הפלייבוק של עזריאלי מהקובץ החדש

# --- מנגנון אימות סיסמה ---
def check_password():
    """בודק אם המשתמש הזין את הסיסמה הנכונה ושומר את הסטטוס."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.markdown("<h3 style='text-align: right; direction: rtl;'>🔒 התחברות לסביבת המחקר</h3>", unsafe_allow_html=True)
        # תיבת הזנת סיסמה
        password = st.text_input("הזן סיסמת גישה:", type="password", key="pwd")
        if password:
            if password == "Scooper2026!":  
                st.session_state["password_correct"] = True
                st.rerun()  
            else:
                st.error("סיסמה שגויה. אנא נסה שוב.")
        return False
    return True

# עצירת רינדור האפליקציה אם הסיסמה טרם הוזנה בהצלחה
if not check_password():
    st.stop()

# ==========================================
# 1. הגדרות מערכת ועיצוב RTL מותאם לממשק
# ==========================================
st.set_page_config(page_title="מחברת פרומפטים - מחקר", page_icon="📊", layout="wide")

st.markdown("""
<style>
    /* הגדרות כיווניות עברית */
    .stApp, .stMarkdown, p, h1, h2, h3, h4, h5, h6, label, li, span { 
        direction: rtl; 
        text-align: right !important; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* תפריט הצד - עיצוב כהה ואלגנטי */
    [data-testid="stSidebar"] { 
        direction: rtl;
        background-color: #1E232F;
    }
    [data-testid="stSidebar"] * {
        color: #E2E8F0;
    }
    
    /* יישור תיבות בחירה וטקסט */
    .stSelectbox div, .stTextInput div { direction: rtl; text-align: right; }
    
    /* עיצוב כפתור ההעתקה של בלוק הקוד */
    div[data-testid="stCodeBlock"] { direction: ltr; text-align: left; background-color: #f8f9fa; border-radius: 8px; border: 1px solid #e2e8f0; }
    div[data-testid="stCodeBlock"] code { direction: rtl; text-align: right; color: #1e293b; }
    
    /* עיצוב כפתורי ניווט בסרגל הצד (Radio Buttons) */
    div[role="radiogroup"] > label {
        padding: 10px;
        border-radius: 6px;
        transition: background-color 0.2s;
    }
    div[role="radiogroup"] > label:hover {
        background-color: #2D3748;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. בניית הממשק (UI)
# ==========================================

# --- סרגל צד (Sidebar) ---
with st.sidebar:
    st.markdown("<h2 style='text-align: right; color: #60A5FA; margin-bottom: 20px;'>SCOOPER RESEARCH<br><span style='color: white; font-size: 1.2rem;'>מחברת פרומפטים</span></h2>", unsafe_allow_html=True)
    
    # אזור בחירות (לקוח, חודש)
    st.markdown("<span style='color: #94A3B8; font-size: 0.9rem;'>שם הלקוח</span>", unsafe_allow_html=True)
    client_selected = st.selectbox(" ", ["קבוצת עזריאלי", "קוקה-קולה (CBC) (בקרוב)"], label_visibility="collapsed")
    
    st.markdown("<span style='color: #94A3B8; font-size: 0.9rem;'>חודש הדוח</span>", unsafe_allow_html=True)
    month_selected = st.text_input(" ", "מאי 2026", label_visibility="collapsed")
    
    st.markdown("<hr style='border-color: #334155; margin-top: 20px;'>", unsafe_allow_html=True)
    
    # תפריט ניווט שלבים (מופיע רק אם נבחר עזריאלי)
    selected_step_title = None
    if client_selected == "קבוצת עזריאלי":
        step_keys = list(azrieli_workflow.keys())
        st.markdown("<span style='color: #94A3B8; font-size: 0.9rem;'>התקדמות העבודה</span>", unsafe_allow_html=True)
        selected_step_key = st.radio(" ", step_keys, label_visibility="collapsed")
        
        # חישוב התקדמות ויזואלי (X מתוך 11)
        current_idx = step_keys.index(selected_step_key) + 1
        total_steps = len(step_keys)
        st.markdown(f"<div style='color: #10B981; font-weight: bold; margin-bottom: 10px;'>{current_idx} / {total_steps}</div>", unsafe_allow_html=True)
    else:
        st.info("הפלייבוק של CBC יתווסף בקרוב.")

# --- אזור מרכזי (Main Area) ---
if client_selected == "קבוצת עזריאלי" and selected_step_key:
    step_data = azrieli_workflow[selected_step_key] # שימוש בנתונים שיובאו מהקובץ החיצוני
    
    # כותרת עליונה של השלב
    st.markdown(f"<h5 style='color: #64748B;'>שקף {current_idx} מתוך {total_steps}</h5>", unsafe_allow_html=True)
    st.markdown(f"<h1>{step_data['title']}</h1>", unsafe_allow_html=True)
    
    st.divider()
    
    # תיבות מידע לאנליסט
    col_info1, col_info2 = st.columns([1, 1])
    with col_info1:
        st.info(f"**📂 קבצים נדרשים מסקופר/מערכת הניטור:**\n\n{step_data['files_needed']}")
    with col_info2:
        st.warning(f"**📋 הנחיות לאנליסט:**\n\n{step_data['instructions']}")
    
    st.markdown("### פרומפט לשליחה ל-AI")
    st.markdown("העתק את הטקסט בתיבה מטה (באמצעות סמל ההעתקה בצד ימין למעלה של התיבה) והדבק אותו במודל ה-AI יחד עם הקבצים הנדרשים.")
    
    # הצגת הפרומפט בתוך אלמנט קוד
    st.code(step_data['prompt'], language="markdown")

else:
    if client_selected != "קבוצת עזריאלי":
        st.title("🚧 אזור בבנייה")
        st.markdown("הפלייבוק הייעודי ללקוח זה יוטמע במערכת בקרוב. אנא בחר ב'קבוצת עזריאלי' כדי לראות את סביבת העבודה הפעילה.")
