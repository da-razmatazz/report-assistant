import streamlit as st
from azrieli_playbook import azrieli_workflow

# --- מנגנון אימות סיסמה ---
def check_password():
    """בודק אם המשתמש הזין את הסיסמה הנכונה ושומר את הסטטוס."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.markdown("""
        <div style='text-align: right; direction: rtl; background-color: #FFF7ED; padding: 20px; border-radius: 12px; border: 1px solid #FFEDD5; max-width: 400px; margin: auto; margin-top: 50px; box-shadow: 0 4px 15px rgba(249, 115, 22, 0.05);'>
            <h2 style='color: #EA580C; margin-bottom: 15px;'>🔒 כניסה למערכת</h2>
        </div>
        """, unsafe_allow_html=True)
        
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
# 1. הגדרות מערכת ועיצוב RTL מותאם לממשק (Yellow-Orange-White Theme)
# ==========================================
st.set_page_config(page_title="Raz Analytics - Report Assistant", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    /* הגדרות כיווניות עברית */
    .stApp, .stMarkdown, p, h1, h2, h3, h4, h5, h6, label, li, span { 
        direction: rtl; 
        text-align: right !important; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* רקע כללי לבן-נקי */
    .stApp {
        background-color: #FAFAFA;
    }
    
    /* תפריט הצד - גוון שמנת עדין עם מסגרת צהובה */
    [data-testid="stSidebar"] { 
        background-color: #FFFCF2;
        border-left: 1px solid #FEF08A;
    }
    
    /* צבע טקסט כללי בתפריט הצד - אפור כהה/כחלחל לקריאות מקסימלית */
    [data-testid="stSidebar"] * {
        color: #334155 !important;
    }
    
    /* יישור תיבות בחירה וטקסט */
    .stSelectbox div, .stTextInput div { direction: rtl; text-align: right; }
    
    /* עיצוב כפתור ההעתקה ובלוק הקוד - מראה הייטקי מואר */
    div[data-testid="stCodeBlock"] { 
        direction: ltr; 
        text-align: left; 
        background-color: #FFFFFF; 
        border-radius: 12px; 
        border: 1px solid #FDE047; 
        box-shadow: 0 4px 15px rgba(250, 204, 21, 0.08);
        padding: 5px;
    }
    div[data-testid="stCodeBlock"] code { 
        direction: rtl; 
        text-align: right; 
        color: #1E293B; 
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    /* עיצוב כפתורי ניווט בסרגל הצד (Radio Buttons) */
    div[role="radiogroup"] > label {
        padding: 12px 15px;
        background-color: #FFFFFF;
        border: 1px solid #FEF08A;
        border-radius: 8px;
        margin-bottom: 8px;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
        cursor: pointer;
    }
    div[role="radiogroup"] > label:hover {
        background-color: #FEF08A;
        border-color: #FACC15;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(250, 204, 21, 0.15);
    }
    
    /* התאמת קו מפריד */
    hr {
        border-color: #FEF08A !important;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. בניית הממשק (UI)
# ==========================================

# --- סרגל צד (Sidebar) ---
with st.sidebar:
    # כותרת המערכת החדשה בעיצוב גרדיאנט
    st.markdown("""
    <div style='margin-bottom: 25px;'>
        <h1 style='text-align: right; background: -webkit-linear-gradient(45deg, #EA580C, #FACC15); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; margin-bottom: 0; font-size: 2.2rem;'>Raz Analytics</h1>
        <span style='color: #64748B; font-size: 1.1rem; font-weight: 600; letter-spacing: 0.5px;'>Report Assistant</span>
    </div>
    """, unsafe_allow_html=True)
    
    # אזור בחירות (לקוח, חודש)
    st.markdown("<span style='color: #64748B; font-size: 0.9rem; font-weight: bold;'>שם הלקוח</span>", unsafe_allow_html=True)
    client_selected = st.selectbox(" ", ["קבוצת עזריאלי", "קוקה-קולה (CBC) (בקרוב)"], label_visibility="collapsed")
    
    st.markdown("<span style='color: #64748B; font-size: 0.9rem; font-weight: bold;'>חודש הדוח</span>", unsafe_allow_html=True)
    month_selected = st.text_input(" ", "מאי 2026", label_visibility="collapsed")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # תפריט ניווט שלבים
    selected_step_key = None
    if client_selected == "קבוצת עזריאלי":
        step_keys = list(azrieli_workflow.keys())
        st.markdown("<span style='color: #64748B; font-size: 0.95rem; font-weight: bold;'>התקדמות העבודה</span>", unsafe_allow_html=True)
        selected_step_key = st.radio(" ", step_keys, label_visibility="collapsed")
        
        # חישוב התקדמות ויזואלי (X מתוך 11) - בצבע כתום מעוצב
        current_idx = step_keys.index(selected_step_key) + 1
        total_steps = len(step_keys)
        st.markdown(f"""
        <div style='margin-top: 15px; padding: 10px; background-color: #FFF7ED; border-radius: 8px; text-align: center; border: 1px dashed #FDBA74;'>
            <span style='color: #EA580C; font-weight: bold; font-size: 1.1rem;'>שלב {current_idx} מתוך {total_steps}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("הפלייבוק של CBC יתווסף בקרוב.")

# --- אזור מרכזי (Main Area) ---
if client_selected == "קבוצת עזריאלי" and selected_step_key:
    step_data = azrieli_workflow[selected_step_key]
    
    # כותרת עליונה של השלב
    st.markdown(f"<h4 style='color: #F59E0B; font-weight: 600; margin-bottom: 0;'>שקף {current_idx} / {total_steps}</h4>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='color: #0F172A; font-weight: 800; margin-top: 5px;'>{step_data['title']}</h1>", unsafe_allow_html=True)
    
    st.markdown("<hr style='margin-top: 10px; margin-bottom: 30px;'>", unsafe_allow_html=True)
    
    # עיצוב מותאם אישית לתיבות המידע במקום st.info/st.warning הבסיסיים
    files_needed_formatted = step_data['files_needed'].replace('\n', '<br>')
    instructions_formatted = step_data['instructions'].replace('\n', '<br>')
    
    col_info1, col_info2 = st.columns([1, 1])
    
    with col_info1:
        st.markdown(f"""
        <div style="background-color: #FFFBEB; border-right: 5px solid #FACC15; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.03); height: 100%;">
            <h4 style="color: #CA8A04; margin-top: 0; display: flex; align-items: center; gap: 8px;">📂 קבצים נדרשים:</h4>
            <p style="color: #334155; margin-bottom: 0; font-size: 1.05rem; line-height: 1.5;">{files_needed_formatted}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_info2:
        st.markdown(f"""
        <div style="background-color: #FFF7ED; border-right: 5px solid #F97316; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.03); height: 100%;">
            <h4 style="color: #C2410C; margin-top: 0; display: flex; align-items: center; gap: 8px;">📋 הנחיות לאנליסט:</h4>
            <p style="color: #334155; margin-bottom: 0; font-size: 1.05rem; line-height: 1.5;">{instructions_formatted}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='color: #0F172A;'>🤖 פרומפט לשליחה למודל</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B; font-size: 1.05rem;'>העתק את הטקסט בתיבה מטה (באמצעות סמל ההעתקה בצד ימין למעלה של התיבה) והדבק אותו במודל ה-AI יחד עם הקבצים הנדרשים.</p>", unsafe_allow_html=True)
    
    # הצגת הפרומפט בתוך אלמנט קוד שיש לו כפתור "העתק" מובנה
    st.code(step_data['prompt'], language="markdown")

else:
    if client_selected != "קבוצת עזריאלי":
        st.markdown("""
        <div style='text-align: center; margin-top: 100px;'>
            <h1 style='color: #0F172A;'>🚧 אזור בבנייה</h1>
            <p style='color: #64748B; font-size: 1.2rem;'>הפלייבוק הייעודי ללקוח זה יוטמע במערכת בקרוב. אנא בחר ב'קבוצת עזריאלי' כדי לראות את סביבת העבודה הפעילה.</p>
        </div>
        """, unsafe_allow_html=True)
