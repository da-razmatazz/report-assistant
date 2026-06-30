import streamlit as st
from azrieli_playbook import azrieli_workflow

# --- מנגנון אימות סיסמה ---
def check_password():
    """בודק אם המשתמש הזין את הסיסמה הנכונה ושומר את הסטטוס."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.markdown("""
        <div style='text-align: right; direction: rtl; background-color: #FFFFFF; padding: 40px; border-radius: 16px; border: 1px solid #E2E8F0; max-width: 450px; margin: 80px auto 0; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);'>
            <div style='display: flex; justify-content: center; margin-bottom: 20px;'>
                <span style='font-size: 48px;'>🔒</span>
            </div>
            <h2 style='color: #1E293B; margin-bottom: 10px; font-weight: 800; text-align: center; font-family: "Heebo", sans-serif;'>כניסה למערכת</h2>
            <p style='color: #64748B; text-align: center; margin-bottom: 30px; font-size: 1.1rem; font-family: "Heebo", sans-serif;'>אנא הזן את סיסמת הגישה כדי להמשיך</p>
        </div>
        """, unsafe_allow_html=True)
        
        # שימוש בעמודות כדי למרכז את שדה הסיסמה
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            password = st.text_input("הזן סיסמת גישה:", type="password", key="pwd", label_visibility="collapsed", placeholder="הקלד סיסמה כאן...")
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
# 1. הגדרות מערכת ועיצוב RTL פרימיום מותאם אישית
# ==========================================
st.set_page_config(page_title="Raz Analytics - Report Assistant", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    /* ייבוא פונט Heebo מ-Google Fonts לקריאות אופטימלית ומראה מודרני */
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;700;800&display=swap');

    /* הגדרות כלליות */
    .stApp, .stMarkdown, p, h1, h2, h3, h4, h5, h6, label, li, span { 
        direction: rtl; 
        text-align: right !important; 
        font-family: 'Heebo', sans-serif !important;
    }
    
    /* רקע כללי - גוון אפור-כחלחל סופר עדין (Slate 50) למראה SaaS מתקדם */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* תפריט הצד - לבן נקי עם הצללה ומסגרת מינימליסטית */
    [data-testid="stSidebar"] { 
        background-color: #FFFFFF !important;
        border-left: 1px solid #E2E8F0;
        box-shadow: -4px 0 15px rgba(0, 0, 0, 0.02);
    }
    
    /* צבעי טקסט - אפור פחם לקריאות גבוהה ללא אימוץ עיניים */
    [data-testid="stSidebar"] * {
        color: #334155 !important;
    }
    
    /* תיבות בחירה וטקסט (Inputs) */
    .stSelectbox div, .stTextInput div { 
        direction: rtl; 
        text-align: right; 
    }
    .stSelectbox>div>div>div, .stTextInput>div>div>input {
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        color: #1E293B;
    }
    .stSelectbox>div>div>div:focus-within, .stTextInput>div>div>input:focus {
        border-color: #F97316 !important;
        box-shadow: 0 0 0 2px rgba(249, 115, 22, 0.2) !important;
    }
    
    /* עיצוב כפתורי ניווט בסרגל הצד (Radio Buttons) - מראה תפריט SaaS צדדי */
    div[role="radiogroup"] {
        gap: 8px;
    }
    div[role="radiogroup"] > label {
        padding: 12px 16px;
        background-color: #FFFFFF;
        border: 1px solid #F1F5F9;
        border-radius: 8px;
        margin-bottom: 4px;
        transition: all 0.2s ease-in-out;
        cursor: pointer;
        display: flex;
        align-items: center;
    }
    div[role="radiogroup"] > label:hover {
        background-color: #F8FAFC;
        border-color: #E2E8F0;
        transform: translateX(-3px);
    }
    /* עיצוב המצב הלחוץ/פעיל של הרדיו באטון בעזרת CSS מתקדם */
    div[role="radiogroup"] > label:has(input:checked) {
        background-color: #FFF7ED !important;
        border: 1px solid #FFEDD5 !important;
        border-right: 4px solid #F97316 !important;
        box-shadow: 0 4px 6px -1px rgba(249, 115, 22, 0.1);
    }
    div[role="radiogroup"] > label:has(input:checked) p {
        color: #C2410C !important;
        font-weight: 700 !important;
    }
    
    /* עיצוב כפתור ההעתקה ובלוק הקוד - פרימיום */
    div[data-testid="stCodeBlock"] { 
        direction: ltr; /* משאיר את כפתור ההעתקה למעלה מימין */
        text-align: left; 
        background-color: #FFFFFF; 
        border-radius: 12px; 
        border: 1px solid #E2E8F0; 
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        padding: 8px;
        transition: border-color 0.2s;
    }
    div[data-testid="stCodeBlock"]:hover {
        border-color: #FACC15;
    }
    div[data-testid="stCodeBlock"] pre {
        background-color: transparent;
    }
    div[data-testid="stCodeBlock"] code { 
        direction: rtl; 
        text-align: right; 
        color: #1E293B; 
        font-size: 1.05rem;
        line-height: 1.7;
        font-family: 'Heebo', monospace; /* משלב נראות קוד עם קריאות עברית */
    }
    
    /* קו מפריד נקי */
    hr {
        border-color: #E2E8F0 !important;
        margin: 24px 0 !important;
    }
    
    /* התאמת צבע כפתור ההעתקה */
    button[title="Copy to clipboard"] {
        background-color: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 6px !important;
    }
    button[title="Copy to clipboard"]:hover {
        background-color: #FEF08A !important;
        border-color: #FACC15 !important;
        color: #CA8A04 !important;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. בניית הממשק (UI)
# ==========================================

# --- סרגל צד (Sidebar) ---
with st.sidebar:
    # כותרת מערכת חדשה - טייפוגרפיה חזקה וגרדיאנט יוקרתי
    st.markdown("""
    <div style='margin-bottom: 30px; padding: 10px 0;'>
        <h1 style='text-align: right; background: linear-gradient(135deg, #F97316 0%, #F59E0B 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; margin-bottom: 5px; font-size: 2.2rem; letter-spacing: -0.5px;'>Raz Analytics</h1>
        <span style='color: #64748B; font-size: 1rem; font-weight: 500; letter-spacing: 1px; text-transform: uppercase;'>Report Assistant</span>
    </div>
    """, unsafe_allow_html=True)
    
    # אזור בחירות (לקוח, חודש) עם תגיות מעוצבות
    st.markdown("<p style='color: #475569; font-size: 0.9rem; font-weight: 700; margin-bottom: 5px;'>🏢 לקוח</p>", unsafe_allow_html=True)
    client_selected = st.selectbox(" ", ["קבוצת עזריאלי", "קוקה-קולה (CBC) (בקרוב)"], label_visibility="collapsed")
    
    st.markdown("<p style='color: #475569; font-size: 0.9rem; font-weight: 700; margin-bottom: 5px; margin-top: 15px;'>📅 חודש הדוח</p>", unsafe_allow_html=True)
    month_selected = st.text_input(" ", "מאי 2026", label_visibility="collapsed")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # תפריט ניווט שלבים
    selected_step_key = None
    if client_selected == "קבוצת עזריאלי":
        step_keys = list(azrieli_workflow.keys())
        st.markdown("<p style='color: #475569; font-size: 1rem; font-weight: 800; margin-bottom: 15px;'>🔄 תוכנית עבודה</p>", unsafe_allow_html=True)
        selected_step_key = st.radio(" ", step_keys, label_visibility="collapsed")
        
        # חישוב התקדמות ויזואלי - עיצוב יוקרתי ונקי
        current_idx = step_keys.index(selected_step_key) + 1
        total_steps = len(step_keys)
        progress_percentage = int((current_idx / total_steps) * 100)
        
        st.markdown(f"""
        <div style='margin-top: 30px; padding: 20px 15px; background-color: #FFFFFF; border-radius: 12px; border: 1px solid #F1F5F9; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;'>
                <span style='color: #64748B; font-size: 0.85rem; font-weight: 600;'>התקדמות</span>
                <span style='color: #EA580C; font-weight: 700; font-size: 0.9rem;'>{current_idx} / {total_steps}</span>
            </div>
            <div style='width: 100%; background-color: #F1F5F9; border-radius: 999px; height: 6px;'>
                <div style='background: linear-gradient(90deg, #F97316, #FACC15); width: {progress_percentage}%; height: 6px; border-radius: 999px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("הפלייבוק של CBC יתווסף בקרוב.")

# --- אזור מרכזי (Main Area) ---
if client_selected == "קבוצת עזריאלי" and selected_step_key:
    step_data = azrieli_workflow[selected_step_key]
    
    # כותרת עליונה של השלב
    st.markdown(f"""
    <div style='margin-bottom: 30px;'>
        <span style='background-color: #FFF7ED; color: #EA580C; padding: 4px 12px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; border: 1px solid #FFEDD5;'>שלב {current_idx} מתוך {total_steps}</span>
        <h1 style='color: #0F172A; font-weight: 800; font-size: 2.5rem; margin-top: 15px; margin-bottom: 0;'>{step_data['title']}</h1>
    </div>
    """, unsafe_allow_html=True)
        
    # עיצוב מותאם אישית לתיבות המידע - כרטיסיות מודרניות
    files_needed_formatted = step_data['files_needed'].replace('\n', '<br>')
    instructions_formatted = step_data['instructions'].replace('\n', '<br>')
    
    col_info1, col_info2 = st.columns([1, 1])
    
    with col_info1:
        st.markdown(f"""
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-right: 4px solid #FACC15; padding: 24px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02), 0 2px 4px -1px rgba(0,0,0,0.02); height: 100%;">
            <h4 style="color: #0F172A; font-weight: 700; margin-top: 0; margin-bottom: 12px; display: flex; align-items: center; gap: 10px; font-size: 1.1rem;">
                <span style="font-size: 1.3rem;">📂</span> קבצים נדרשים
            </h4>
            <p style="color: #475569; margin-bottom: 0; font-size: 1.05rem; line-height: 1.6;">{files_needed_formatted}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col_info2:
        st.markdown(f"""
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-right: 4px solid #F97316; padding: 24px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02), 0 2px 4px -1px rgba(0,0,0,0.02); height: 100%;">
            <h4 style="color: #0F172A; font-weight: 700; margin-top: 0; margin-bottom: 12px; display: flex; align-items: center; gap: 10px; font-size: 1.1rem;">
                <span style="font-size: 1.3rem;">📋</span> הנחיות לאנליסט
            </h4>
            <p style="color: #475569; margin-bottom: 0; font-size: 1.05rem; line-height: 1.6;">{instructions_formatted}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="margin-bottom: 15px;">
        <h3 style='color: #0F172A; font-weight: 800; font-size: 1.5rem; display: inline-flex; align-items: center; gap: 10px;'>
            <span style="font-size: 1.6rem;">🤖</span> פרומפט לשליחה למודל
        </h3>
        <p style='color: #64748B; font-size: 1rem; margin-top: 5px;'>לחץ על סמל ההעתקה בצד שמאל למעלה של התיבה כדי להעתיק את הפרומפט במלואו.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # הצגת הפרומפט בתוך אלמנט קוד שיש לו כפתור "העתק" מובנה
    st.code(step_data['prompt'], language="markdown")

else:
    if client_selected != "קבוצת עזריאלי":
        st.markdown("""
        <div style='text-align: center; margin-top: 120px; background-color: #FFFFFF; padding: 60px; border-radius: 20px; border: 1px dashed #CBD5E1; max-width: 600px; margin-left: auto; margin-right: auto;'>
            <span style='font-size: 64px;'>🚧</span>
            <h1 style='color: #0F172A; font-weight: 800; margin-top: 20px;'>אזור בבנייה</h1>
            <p style='color: #64748B; font-size: 1.1rem; line-height: 1.6; margin-top: 15px;'>הפלייבוק הייעודי ללקוח זה יוטמע במערכת בקרוב. אנא בחר ב<strong>'קבוצת עזריאלי'</strong> מתפריט הצד כדי לראות את סביבת העבודה הפעילה.</p>
        </div>
        """, unsafe_allow_html=True)
