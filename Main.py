import streamlit as st
from azrieli_playbook import azrieli_workflow

# --- מנגנון אימות סיסמה ---
def check_password():
    """בודק אם המשתמש הזין את הסיסמה הנכונה ושומר את הסטטוס."""
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.markdown("""
        <div style='text-align: right; direction: rtl; background-color: #FFFFFF; padding: 50px 40px; border-radius: 24px; border: 1px solid #E2E8F0; max-width: 480px; margin: 100px auto 0; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.05), 0 10px 10px -5px rgba(0,0,0,0.02);'>
            <div style='text-align: center; margin-bottom: 25px;'>
                <div style='background: linear-gradient(135deg, #7C2D12 0%, #EA580C 50%, #FBBF24 100%); width: 70px; height: 70px; border-radius: 20px; display: flex; align-items: center; justify-content: center; margin: 0 auto; box-shadow: 0 10px 15px -3px rgba(234, 88, 12, 0.2);'>
                    <span style='font-size: 32px;'>🔒</span>
                </div>
            </div>
            <h2 style='color: #0F172A; margin-bottom: 8px; font-weight: 800; text-align: center; font-size: 1.8rem; font-family: "Heebo", sans-serif;'>כניסה מאובטחת</h2>
            <p style='color: #64748B; text-align: center; margin-bottom: 35px; font-size: 1rem; font-family: "Heebo", sans-serif;'>אנא הזן את סיסמת הגישה של Raz Analytics</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            password = st.text_input("הזן סיסמת גישה:", type="password", key="pwd", label_visibility="collapsed", placeholder="הקלד את סיסמת הגישה כאן...")
            if password:
                if password == "Scooper2026!":  
                    st.session_state["password_correct"] = True
                    st.rerun()  
                else:
                    st.markdown("<p style='color: #EF4444; font-weight: 600; text-align: center; margin-top: 10px;'>❌ סיסמה שגויה. נסה שוב.</p>", unsafe_allow_html=True)
        return False
    return True

if not check_password():
    st.stop()

# ==========================================
# 1. הגדרות מערכת ועיצוב אוברהול אסתטי (Complete Overhaul)
# ==========================================
st.set_page_config(page_title="Raz Analytics - Report Assistant", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;500;600;700;800;900&display=swap');

    /* הגדרות כיווניות וקריאות גלובליות */
    .stApp, .stMarkdown, p, h1, h2, h3, h4, h5, h6, label, li, span { 
        direction: rtl; 
        text-align: right !important; 
        font-family: 'Heebo', sans-serif !important;
    }
    
    /* רקע האפליקציה - אפור-משי סופר נקי ויוקרתי */
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* ==========================================
       מהפך ל-SIDEBAR: קונספט עדשת משקפי שמש כהה
       ========================================== */
    [data-testid="stSidebar"] { 
        background-color: #0F172A !important; /* אפור-פחם עמוק ומקוטב */
        border-left: 1px solid #1E293B;
        box-shadow: -8px 0 30px rgba(0, 0, 0, 0.25);
    }
    
    /* התאמת כל הטקסטים בתוך ה-Sidebar למצב Dark */
    [data-testid="stSidebar"] * {
        color: #E2E8F0 !important;
    }
    
    /* הגדרת תיבות קלט בתוך הסיידבר */
    [data-testid="stSidebar"] .stSelectbox div, [data-testid="stSidebar"] .stTextInput div { 
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }
    [data-testid="stSidebar"] input, [data-testid="stSidebar"] select {
        color: #FFFFFF !important;
    }

    /* עיצוב כפתורי הרדיו (השלבים) בתוך ה-Sidebar הכהה */
    div[role="radiogroup"] {
        gap: 10px !important;
        padding-top: 10px;
    }
    div[role="radiogroup"] > label {
        padding: 14px 18px !important;
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        margin-bottom: 6px !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    div[role="radiogroup"] > label:hover {
        background-color: #273549 !important;
        border-color: #D97706 !important;
        transform: translateX(-4px) !important;
    }
    
    /* אפקט עדשה מתכהה מטאלית במצב לחוץ (Active State) */
    div[role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(135deg, #7C2D12 0%, #EA580C 60%, #F59E0B 100%) !important;
        border: 1px solid #F97316 !important;
        box-shadow: 0 8px 20px rgba(234, 88, 12, 0.35) !important;
        transform: translateX(-6px) !important;
    }
    div[role="radiogroup"] > label:has(input:checked) p {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }
    
    /* ==========================================
       מהפך לבלוק הקוד (פרומפט): מקסימום ניגודיות
       ========================================== */
    div[data-testid="stCodeBlock"] { 
        direction: ltr !important; 
        text-align: left !important; 
        background-color: #0B0F19 !important; /* רקע קוד כהה אבסולוטי לעומת האפליקציה הבהירה */
        border: 2px solid #1E293B !important; 
        border-radius: 16px !important; 
        box-shadow: 0 12px 25px -5px rgba(0, 0, 0, 0.15), 0 8px 10px -6px rgba(0, 0, 0, 0.1) !important;
        padding: 20px !important;
        margin-top: 15px;
    }
    div[data-testid="stCodeBlock"] code { 
        direction: rtl !important; 
        text-align: right !important; 
        color: #F8FAFC !important; /* טקסט בהיר וחד כקריסטל */
        font-size: 1.1rem !important;
        line-height: 1.8 !important;
        font-family: 'Consolas', 'Courier New', monospace !important;
    }
    
    /* כפתור העתקה של המודל */
    button[title="Copy to clipboard"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    button[title="Copy to clipboard"]:hover {
        background-color: #EA580C !important;
        border-color: #F97316 !important;
    }

    /* קווים מפרידים עדינים ומודרניים */
    hr {
        border-color: #E2E8F0 !important;
        margin: 32px 0 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. בניית הממשק (UI)
# ==========================================

# --- סרגל צד (Sidebar) ---
with st.sidebar:
    # כותרת לוגו פרימיום בתוך תפריט הצד הכהה
    st.markdown("""
    <div style='margin-bottom: 35px; padding: 15px 0 5px 0;'>
        <h1 style='text-align: right; background: linear-gradient(135deg, #FFEDD5 0%, #F59E0B 50%, #EA580C 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; margin-bottom: 0; font-size: 2.4rem; letter-spacing: -0.5px;'>Raz Analytics</h1>
        <div style='color: #94A3B8; font-size: 0.95rem; font-weight: 600; letter-spacing: 1.5px; margin-top: 5px; text-transform: uppercase; opacity: 0.8;'>Report Assistant</div>
    </div>
    """, unsafe_allow_html=True)
    
    # אזור בחירות (לקוח, חודש)
    st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; font-weight: 700; margin-bottom: 6px; letter-spacing: 0.5px;'>🏢 פרופיל לקוח פעיל</p>", unsafe_allow_html=True)
    client_selected = st.selectbox(" ", ["קבוצת עזריאלי", "קוקה-קולה (CBC) (בקרוב)"], label_visibility="collapsed")
    
    st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; font-weight: 700; margin-bottom: 6px; margin-top: 20px; letter-spacing: 0.5px;'>📅 מחזור דוח חודשי</p>", unsafe_allow_html=True)
    month_selected = st.text_input(" ", "מאי 2026", label_visibility="collapsed")
    
    st.markdown("<hr style='border-color: #1E293B !important;'>", unsafe_allow_html=True)
    
    # תפריט ניווט שלבים
    selected_step_key = None
    if client_selected == "קבוצת עזריאלי":
        step_keys = list(azrieli_workflow.keys())
        st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; font-weight: 700; margin-bottom: 12px; letter-spacing: 0.5px;'>🗺️ מפת שלבי עבודה</p>", unsafe_allow_html=True)
        selected_step_key = st.radio(" ", step_keys, label_visibility="collapsed")
        
        # מד התקדמות (Progress Tracker) בעיצוב מתוחכם
        current_idx = step_keys.index(selected_step_key) + 1
        total_steps = len(step_keys)
        progress_percentage = int((current_idx / total_steps) * 100)
        
        st.markdown(f"""
        <div style='margin-top: 35px; padding: 22px 18px; background-color: #1E293B; border-radius: 16px; border: 1px solid #334155; box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);'>
            <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; direction: rtl;'>
                <span style='color: #94A3B8; font-size: 0.85rem; font-weight: 600;'>קצב התקדמות פלייבוק</span>
                <span style='color: #FBBF24; font-weight: 800; font-size: 1rem;'>{current_idx} / {total_steps}</span>
            </div>
            <div style='width: 100%; background-color: #0F172A; border-radius: 999px; height: 8px; overflow: hidden;'>
                <div style='background: linear-gradient(90deg, #EA580C, #FBBF24); width: {progress_percentage}%; height: 8px; border-radius: 999px;'></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("הפלייבוק של CBC יתווסף בקרוב.")

# --- אזור מרכזי (Main Area) ---
if client_selected == "קבוצת עזריאלי" and selected_step_key:
    step_data = azrieli_workflow[selected_step_key]
    
    # כותרת עליונה של השלב הראשי
    st.markdown(f"""
    <div style='margin-bottom: 35px; margin-top: 10px;'>
        <div style='display: inline-block; background: linear-gradient(135deg, #7C2D12 0%, #EA580C 100%); color: #FFFFFF; padding: 6px 16px; border-radius: 30px; font-size: 0.85rem; font-weight: 800; border: 1px solid #EA580C; box-shadow: 0 4px 10px rgba(234,88,12,0.15);'>שקף מצגת {current_idx} מתוך {total_steps}</div>
        <h1 style='color: #0F172A; font-weight: 900; font-size: 2.8rem; margin-top: 18px; margin-bottom: 0; letter-spacing: -0.5px;'>{step_data['title']}</h1>
    </div>
    """, unsafe_allow_html=True)
        
    # תיבות מידע מורחבות ומרווחות (Overhauled Cards)
    files_needed_formatted = step_data['files_needed'].replace('\n', '<br>')
    instructions_formatted = step_data['instructions'].replace('\n', '<br>')
    
    col_info1, col_info2 = st.columns([1, 1])
    
    with col_info1:
        st.markdown(f"""
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-right: 5px solid #FACC15; padding: 32px; border-radius: 16px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.02), 0 8px 10px -6px rgba(0,0,0,0.02); height: 100%;">
            <h4 style="color: #0F172A; font-weight: 800; margin-top: 0; margin-bottom: 15px; display: flex; align-items: center; gap: 12px; font-size: 1.2rem;">
                <span style="font-size: 1.5rem;">📂</span> קבצי מקור לניתוח הדאטה
            </h4>
            <div style="color: #334155; font-size: 1.05rem; line-height: 1.7; font-weight: 400;">{files_needed_formatted}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_info2:
        st.markdown(f"""
        <div style="background-color: #FFFFFF; border: 1px solid #E2E8F0; border-right: 5px solid #EA580C; padding: 32px; border-radius: 16px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.02), 0 8px 10px -6px rgba(0,0,0,0.02); height: 100%;">
            <h4 style="color: #0F172A; font-weight: 800; margin-top: 0; margin-bottom: 15px; display: flex; align-items: center; gap: 12px; font-size: 1.2rem;">
                <span style="font-size: 1.5rem;">📋</span> הנחיות עבודה לאנליסט
            </h4>
            <div style="color: #334155; font-size: 1.05rem; line-height: 1.7; font-weight: 400;">{instructions_formatted}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # כותרת לקוד
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h3 style='color: #0F172A; font-weight: 900; font-size: 1.6rem; display: inline-flex; align-items: center; gap: 12px;'>
            <span style="font-size: 1.8rem;">🤖</span> ארכיטקטורת פרומפט מבוססת תובנה
        </h3>
        <p style='color: #475569; font-size: 1.05rem; margin-top: 5px; font-weight: 400;'>העתק את המבנה המוכן מטה והזן אותו למודל ה-AI יחד עם קבצי הנתונים שחילצת בחלון השיחה.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # יצירת ה-Code Block הכהה והניגודי
    st.code(step_data['prompt'], language="markdown")

else:
    if client_selected != "קבוצת עזריאלי":
        st.markdown("""
        <div style='text-align: center; margin-top: 150px; background-color: #FFFFFF; padding: 80px 40px; border-radius: 24px; border: 1px dashed #CBD5E1; max-width: 650px; margin-left: auto; margin-right: auto; box-shadow: 0 10px 30px rgba(0,0,0,0.02);'>
            <span style='font-size: 72px; display: block; margin-bottom: 15px;'>🚧</span>
            <h1 style='color: #0F172A; font-weight: 900; margin-top: 20px; font-size: 2.2rem;'>מרחב העבודה בבנייה</h1>
            <p style='color: #64748B; font-size: 1.15rem; line-height: 1.7; margin-top: 15px; font-weight: 400;'>הפלייבוק האסטרטגי עבור מותג זה נמצא כעת בשלבי פיתוח ואפיון ממשק.<br>אנא בחר ב-<strong>'קבוצת עזריאלי'</strong> כדי לעבוד בסביבה הפעילה.</p>
        </div>
        """, unsafe_allow_html=True)
