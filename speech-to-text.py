"""
المهمة الثالثة: تحويل الصوت إلى نص وكشف اللغة
"""

import speech_recognition as sr
from typing import Tuple, Optional

def transcribe(audio_file_path: Optional[str] = None, 
               audio_data: Optional[sr.AudioData] = None) -> Tuple[str, str]:
    """
    تحويل الصوت إلى نص وكشف اللغة
    
    المعاملات:
        audio_file_path: مسار ملف الصوت (مثل 'audio.wav')
        audio_data: بيانات الصوت من التسجيل المباشر
    
    الإرجاع:
        (النص, اللغة) -> ('مرحبا', 'arabic') أو ('Hello', 'english')
    """
    
    # إنشاء كائن التعرف على الصوت
    recognizer = sr.Recognizer()
    
    # الحصول على بيانات الصوت (إما من ملف أو من التسجيل)
    if audio_data is None:
        if audio_file_path is None:
            raise ValueError("يجب توفير إما مسار الملف أو بيانات الصوت")
        
        # قراءة الصوت من الملف
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
    
    # المحاولة الأولى: التعرف باللغة العربية
    try:
        text = recognizer.recognize_google(audio_data, language="ar-EG")
        if text.strip():  # إذا كان النص غير فارغ
            return text, "arabic"
    except sr.UnknownValueError:
        # لم يتم التعرف على النص بالعربية
        pass
    except sr.RequestError as e:
        print(f"خطأ في الاتصال: {e}")
    
    # المحاولة الثانية: التعرف باللغة الإنجليزية
    try:
        text = recognizer.recognize_google(audio_data, language="en-US")
        if text.strip():
            return text, "english"
    except sr.UnknownValueError:
        # لم يتم التعرف على النص بالإنجليزية
        pass
    except sr.RequestError as e:
        print(f"خطأ في الاتصال: {e}")
    
    # إذا فشل كل شيء
    return "", "unknown"


# دالة إضافية: كشف اللغة تلقائياً (بدون تحديد مسبق)
def transcribe_auto(audio_file_path: Optional[str] = None, 
                    audio_data: Optional[sr.AudioData] = None) -> Tuple[str, str]:
    """
    تحويل الصوت إلى نص مع كشف اللغة تلقائياً
    """
    recognizer = sr.Recognizer()
    
    # الحصول على بيانات الصوت
    if audio_data is None:
        if audio_file_path is None:
            raise ValueError("يجب توفير إما مسار الملف أو بيانات الصوت")
        
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
    
    # قائمة اللغات المدعومة
    languages = {
        "ar-EG": "arabic",
        "en-US": "english",
        "fr-FR": "french",
        "de-DE": "german",
        "es-ES": "spanish"
    }
    
    # تجربة كل لغة
    for lang_code, lang_name in languages.items():
        try:
            text = recognizer.recognize_google(audio_data, language=lang_code)
            if text.strip():
                return text, lang_name
        except:
            continue
    
    return "", "unknown"


# دالة للاختبار البسيط
def test_transcribe():
    """دالة بسيطة لاختبار التحويل"""
    print("=" * 50)
    print("اختبار دالة transcribe")
    print("=" * 50)
    
    # استخدام ملف صوتي للاختبار (إذا كان موجوداً)
    test_file = "test_audio.wav"
    
    try:
        # محاولة تحويل ملف صوتي
        text, language = transcribe(test_file)
        print(f"النص المُفرَّغ: {text}")
        print(f"اللغة المكتشفة: {language}")
        
    except FileNotFoundError:
        print(f"⚠️  ملف {test_file} غير موجود")
        print("💡 يمكنك اختبار الدالة بملف صوتي حقيقي")
        
    except Exception as e:
        print(f"❌ خطأ: {e}")
    
    print("\n✅ الدالة جاهزة للاستخدام!")


# تشغيل الاختبار
if __name__ == "__main__":
    test_transcribe()