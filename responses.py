"""
responses.py — NLP Intent Recognition & Multi-Language Response Engine
Uses keyword/regex pattern matching with NLTK tokenisation
"""

import re
import random
from datetime import datetime

# ─── Intent Patterns ─────────────────────────────────────────────────────────

INTENT_PATTERNS = {
    "balance": [
        r"\bbalance\b", r"\bshesh\b", r"\bniluva\b", r"\bavailable\b",
        r"\bmoney\b", r"\bfunds\b", r"\baccount amount\b", r"\bखाता शेष\b",
        r"\bబ్యాలెన్స్\b", r"\bhow much\b"
    ],
    "transactions": [
        r"\btransact\b", r"\bhistory\b", r"\bstatement\b", r"\brecent\b",
        r"\bpayment\b", r"\bspent\b", r"\bdebit\b", r"\blast.*transfer\b",
        r"\bలావాదేవీ\b", r"\bलेनदेन\b", r"\bखर्च\b"
    ],
    "loan": [
        r"\bloan\b", r"\bemi\b", r"\bmortgage\b", r"\brepay\b",
        r"\bgriha\b", r"\bhome loan\b", r"\bpersonal loan\b",
        r"\bరుణ\b", r"\bऋण\b", r"\binstalment\b"
    ],
    "credit_card": [
        r"\bcredit card\b", r"\bcard\b", r"\bvisa\b", r"\bmastercard\b",
        r"\bcredit limit\b", r"\bక్రెడిట్\b", r"\bक्रेडिट\b", r"\bdue\b"
    ],
    "support": [
        r"\bsupport\b", r"\bhelp\b", r"\bcontact\b", r"\bcomplaint\b",
        r"\bissue\b", r"\bcustomer care\b", r"\bsahayata\b",
        r"\bసపోర్ట్\b", r"\bसहायता\b", r"\bhelpline\b"
    ],
    "branch": [
        r"\bbranch\b", r"\blocation\b", r"\batm\b", r"\bnear\b",
        r"\baddress\b", r"\bshakha\b", r"\bశాఖ\b", r"\bशाखा\b"
    ],
    "fixed_deposit": [
        r"\bfixed deposit\b", r"\bfd\b", r"\bterm deposit\b",
        r"\bsavings plan\b", r"\bస్థిర\b", r"\bसावधि\b", r"\binvestment\b"
    ],
    "fraud": [
        r"\bfraud\b", r"\bsuspicious\b", r"\bstolen\b", r"\bblock.*card\b",
        r"\blost.*card\b", r"\bscam\b", r"\bమోసం\b", r"\bधोखाधड़ी\b",
        r"\bunauthorized\b", r"\bhacked\b"
    ],
    "upi": [
        r"\bupi\b", r"\bpay\b", r"\bsend money\b", r"\bpayment.*fail\b",
        r"\bgpay\b", r"\bphonepe\b", r"\bpaytm\b", r"\btransfer\b"
    ],
    "interest_rate": [
        r"\binterest\b", r"\brate\b", r"\brog rate\b", r"\brepo\b",
        r"\bవడ్డీ\b", r"\bब्याज\b"
    ],
    "greeting": [
        r"\bhello\b", r"\bhi\b", r"\bhey\b", r"\bnamaste\b",
        r"\bనమస్కారం\b", r"\bनमस्ते\b", r"\bgood morning\b",
        r"\bgood afternoon\b", r"\bgood evening\b"
    ],
    "thanks": [
        r"\bthank\b", r"\bthanks\b", r"\bdhanyavad\b", r"\bధన్యవాదాలు\b",
        r"\bधन्यवाद\b", r"\bgreat\b", r"\bawesome\b", r"\bperfect\b"
    ],
    "bye": [
        r"\bbye\b", r"\bgoodbye\b", r"\bsee you\b", r"\bexit\b",
        r"\bclose\b", r"\bvidai\b"
    ]
}


def detect_intent(text: str) -> str:
    """Run regex patterns and return best-matched intent."""
    text_lower = text.lower()
    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                return intent
    return "unknown"


# ─── Response Templates (English, Hindi, Telugu) ─────────────────────────────

def _now():
    return datetime.now().strftime("%d %b %Y, %I:%M %p")


RESPONSES = {
    "English": {
        "greeting": lambda user: (
            f"Hello {user['full_name'].split()[0]}! 👋 Welcome to NeoBank AI Assistant.\n\n"
            "I can help you with:\n"
            "• 💰 Account Balance\n• 📋 Transactions\n• 🏠 Loans\n"
            "• 💳 Credit Card\n• 📈 Fixed Deposits\n• 🎧 Customer Support\n\n"
            "How can I assist you today?"
        ),
        "balance": lambda user: (
            f"**Account Balance — {_now()}**\n\n"
            f"👤 Account Holder: {user['full_name']}\n"
            f"🏦 Account No: {user['acct_no']}\n"
            f"📊 Account Type: Savings Account\n\n"
            "| | Amount |\n|---|---|\n"
            "| 💚 Available Balance | ₹ 1,42,580.00 |\n"
            "| 📒 Ledger Balance | ₹ 1,45,000.00 |\n"
            "| 🔒 Blocked Amount | ₹ 2,420.00 |\n\n"
            "✅ Account Status: **Active**"
        ),
        "transactions": lambda user: (
            "**Recent Transactions (Last 10 Days)**\n\n"
            "| Date | Description | Amount | Type |\n|---|---|---|---|\n"
            "| 28 May | Swiggy Order | ₹ 450 | 🔴 Debit |\n"
            "| 27 May | UPI to Suresh | ₹ 5,000 | 🔴 Debit |\n"
            "| 26 May | Salary Credit | ₹ 52,000 | 🟢 Credit |\n"
            "| 25 May | Amazon Shopping | ₹ 1,299 | 🔴 Debit |\n"
            "| 24 May | ATM Withdrawal | ₹ 3,000 | 🔴 Debit |\n"
            "| 23 May | Netflix Sub | ₹ 649 | 🔴 Debit |\n"
            "| 22 May | Electricity Bill | ₹ 1,120 | 🔴 Debit |\n"
            "| 21 May | Cashback | ₹ 250 | 🟢 Credit |\n\n"
            "📧 Full statement sent to your registered email."
        ),
        "loan": lambda user: (
            "**Your Active Loans**\n\n"
            "**🏠 Home Loan**\n"
            "| Field | Details |\n|---|---|\n"
            "| Loan ID | HL-20219876 |\n"
            "| Principal Amount | ₹ 25,00,000 |\n"
            "| Outstanding | ₹ 18,43,200 |\n"
            "| EMI Amount | ₹ 21,500/month |\n"
            "| Next EMI Due | 5 June 2025 |\n"
            "| Tenure Left | 87 months |\n"
            "| Interest Rate | 8.5% p.a. |\n\n"
            "💡 *Tip: Prepayment can reduce your total interest by up to 30%.*"
        ),
        "credit_card": lambda user: (
            "**Credit Card Summary**\n\n"
            "💳 **NeoBank Platinum Visa** — ●●●● ●●●● ●●●● 8832\n\n"
            "| Detail | Value |\n|---|---|\n"
            "| Credit Limit | ₹ 2,00,000 |\n"
            "| Amount Used | ₹ 32,480 |\n"
            "| Available Credit | ₹ 1,67,520 |\n"
            "| Payment Due | ₹ 32,480 |\n"
            "| Due Date | 10 June 2025 |\n"
            "| Reward Points | 4,820 pts |\n\n"
            "⚠️ Pay by due date to avoid interest charges."
        ),
        "support": lambda user: (
            "**Customer Support — NeoBank**\n\n"
            "| Channel | Details |\n|---|---|\n"
            "| 📞 Toll-Free | 1800-XXX-XXXX (24×7) |\n"
            "| 📧 Email | support@neobank.in |\n"
            "| 💬 Live Chat | Available on app |\n"
            "| 🏦 Branch Visit | Mon–Sat, 9AM–4PM |\n\n"
            "**Common Issues:**\n"
            "• Card blocking → Press 1\n"
            "• Dispute/Fraud → Press 2\n"
            "• Account queries → Press 3\n"
            "• Loan queries → Press 4\n\n"
            "Average wait time: **< 2 minutes**"
        ),
        "branch": lambda user: (
            "**NeoBank Branches Near You (Hyderabad)**\n\n"
            "| Branch | Distance | Timings |\n|---|---|---|\n"
            "| 📍 Banjara Hills | 0.8 km | Mon–Sat 9AM–4PM |\n"
            "| 📍 Hitech City | 2.1 km | Mon–Sat 9AM–4PM |\n"
            "| 📍 Jubilee Hills | 3.4 km | Mon–Sat 9AM–4PM |\n"
            "| 📍 Ameerpet | 5.0 km | Mon–Sat 9AM–4PM |\n\n"
            "🏧 **Nearest ATM:** Banjara Hills Main Road (0.3 km)\n\n"
            "📌 *Use NeoBank app for live GPS navigation to branches.*"
        ),
        "fixed_deposit": lambda user: (
            "**Your Fixed Deposits**\n\n"
            "**FD #001 — Active ✅**\n"
            "| Detail | Value |\n|---|---|\n"
            "| Principal | ₹ 50,000 |\n"
            "| Interest Rate | 7.25% p.a. |\n"
            "| Start Date | 15 Jun 2024 |\n"
            "| Maturity Date | 15 Dec 2025 |\n"
            "| Maturity Value | ₹ 53,625 |\n\n"
            "📈 *Current NeoBank FD Rates:*\n"
            "• 1 year: 6.75% | 2 years: 7.00% | 3 years: 7.50%\n\n"
            "💡 Auto-renewal is enabled for your FD."
        ),
        "fraud": lambda user: (
            "⚠️ **FRAUD ALERT — Immediate Action Required**\n\n"
            "**Do NOT share:**\n"
            "❌ OTP / PIN\n"
            "❌ CVV / Card Number\n"
            "❌ Internet Banking Password\n\n"
            "**Immediate Steps:**\n"
            "1. 📞 Call: **1800-XXX-0001** (Fraud Helpline — 24×7)\n"
            "2. 🔒 Block your card: App → Cards → Block Card\n"
            "3. 📧 Email: fraud@neobank.in\n"
            "4. 🏦 Visit nearest branch with ID proof\n\n"
            "⚡ We **never** ask for OTP or passwords. Stay alert!"
        ),
        "upi": lambda user: (
            "**UPI & Payment Services**\n\n"
            "| Feature | Status |\n|---|---|\n"
            "| UPI ID | rajesh@neobank |\n"
            "| Daily Limit | ₹ 1,00,000 |\n"
            "| Used Today | ₹ 5,450 |\n"
            "| Remaining | ₹ 94,550 |\n\n"
            "**Supported Apps:** Google Pay · PhonePe · Paytm · BHIM\n\n"
            "**Payment Failed?**\n"
            "• Wait 30 mins — refund auto-credited\n"
            "• Raise dispute: 1800-XXX-XXXX\n"
            "• Claim via UPI Dispute Portal"
        ),
        "interest_rate": lambda user: (
            "**Current NeoBank Interest Rates**\n\n"
            "| Product | Rate |\n|---|---|\n"
            "| Savings Account | 3.5% p.a. |\n"
            "| Fixed Deposit (1Y) | 6.75% p.a. |\n"
            "| Fixed Deposit (3Y) | 7.50% p.a. |\n"
            "| Home Loan | 8.50% p.a. |\n"
            "| Personal Loan | 12.50% p.a. |\n"
            "| Car Loan | 9.25% p.a. |\n\n"
            "📅 Rates effective as of June 2025. Subject to RBI policy."
        ),
        "thanks": lambda user: random.choice([
            f"You're welcome, {user['full_name'].split()[0]}! 😊 Is there anything else I can help you with?",
            "Happy to help! Let me know if you need anything else. 🏦",
            "Glad I could assist! Your satisfaction is our priority. ✨"
        ]),
        "bye": lambda user: (
            f"Goodbye, {user['full_name'].split()[0]}! 👋\n"
            "Thank you for banking with NeoBank. Have a great day! 🏦"
        ),
        "unknown": lambda user: (
            "I'm sorry, I didn't quite understand that. 🤔\n\n"
            "You can ask me about:\n"
            "• 💰 Account Balance\n"
            "• 📋 Recent Transactions\n"
            "• 🏠 Loan Details\n"
            "• 💳 Credit Card\n"
            "• 📈 Fixed Deposits\n"
            "• 📍 Branch Location\n"
            "• 🎧 Customer Support\n"
            "• 🚨 Report Fraud\n\n"
            "Or use the **Quick Action buttons** on the left! 😊"
        ),
    },

    "Hindi": {
        "greeting": lambda user: (
            f"नमस्ते {user['full_name'].split()[0]} जी! 👋 NeoBank AI असिस्टेंट में आपका स्वागत है।\n\n"
            "मैं आपकी सहायता कर सकता हूं:\n"
            "• 💰 खाता शेष\n• 📋 लेनदेन\n• 🏠 ऋण\n"
            "• 💳 क्रेडिट कार्ड\n• 📈 सावधि जमा\n• 🎧 ग्राहक सेवा\n\n"
            "आज मैं आपकी कैसे सहायता करूं?"
        ),
        "balance": lambda user: (
            f"**खाता शेष — {_now()}**\n\n"
            f"👤 खाताधारक: {user['full_name']}\n"
            f"🏦 खाता संख्या: {user['acct_no']}\n\n"
            "| | राशि |\n|---|---|\n"
            "| 💚 उपलब्ध शेष | ₹ 1,42,580.00 |\n"
            "| 📒 लेजर शेष | ₹ 1,45,000.00 |\n"
            "| 🔒 अवरुद्ध राशि | ₹ 2,420.00 |\n\n"
            "✅ खाता स्थिति: **सक्रिय**"
        ),
        "transactions": lambda user: (
            "**हाल के लेनदेन (पिछले 10 दिन)**\n\n"
            "| दिनांक | विवरण | राशि | प्रकार |\n|---|---|---|---|\n"
            "| 28 मई | Swiggy ऑर्डर | ₹ 450 | 🔴 डेबिट |\n"
            "| 27 मई | UPI भुगतान | ₹ 5,000 | 🔴 डेबिट |\n"
            "| 26 मई | वेतन जमा | ₹ 52,000 | 🟢 क्रेडिट |\n"
            "| 25 मई | Amazon खरीदारी | ₹ 1,299 | 🔴 डेबिट |\n"
            "| 24 मई | ATM निकासी | ₹ 3,000 | 🔴 डेबिट |\n\n"
            "📧 पूरा विवरण आपके ईमेल पर भेजा गया है।"
        ),
        "loan": lambda user: (
            "**आपके सक्रिय ऋण**\n\n"
            "**🏠 गृह ऋण**\n"
            "| विवरण | जानकारी |\n|---|---|\n"
            "| ऋण आईडी | HL-20219876 |\n"
            "| मूल राशि | ₹ 25,00,000 |\n"
            "| बकाया राशि | ₹ 18,43,200 |\n"
            "| मासिक किस्त | ₹ 21,500 |\n"
            "| अगली देय तिथि | 5 जून 2025 |\n"
            "| ब्याज दर | 8.5% प्रति वर्ष |\n\n"
            "💡 *अग्रिम भुगतान से ब्याज में 30% तक की बचत हो सकती है।*"
        ),
        "credit_card": lambda user: (
            "**क्रेडिट कार्ड सारांश**\n\n"
            "💳 **NeoBank Platinum Visa** — ●●●● ●●●● ●●●● 8832\n\n"
            "| विवरण | मूल्य |\n|---|---|\n"
            "| क्रेडिट सीमा | ₹ 2,00,000 |\n"
            "| उपयोग की गई राशि | ₹ 32,480 |\n"
            "| उपलब्ध क्रेडिट | ₹ 1,67,520 |\n"
            "| देय राशि | ₹ 32,480 |\n"
            "| देय तिथि | 10 जून 2025 |\n"
            "| इनाम अंक | 4,820 pts |\n\n"
            "⚠️ ब्याज से बचने के लिए समय पर भुगतान करें।"
        ),
        "support": lambda user: (
            "**ग्राहक सेवा — NeoBank**\n\n"
            "| माध्यम | विवरण |\n|---|---|\n"
            "| 📞 टोल-फ्री | 1800-XXX-XXXX (24×7) |\n"
            "| 📧 ईमेल | support@neobank.in |\n"
            "| 💬 लाइव चैट | ऐप पर उपलब्ध |\n\n"
            "औसत प्रतीक्षा समय: **< 2 मिनट**"
        ),
        "branch": lambda user: (
            "**आपके निकटतम NeoBank शाखाएं**\n\n"
            "| शाखा | दूरी | समय |\n|---|---|---|\n"
            "| 📍 बंजारा हिल्स | 0.8 किमी | सोम–शनि 9AM–4PM |\n"
            "| 📍 हाईटेक सिटी | 2.1 किमी | सोम–शनि 9AM–4PM |\n"
            "| 📍 जुबिली हिल्स | 3.4 किमी | सोम–शनि 9AM–4PM |\n\n"
            "🏧 **निकटतम ATM:** बंजारा हिल्स (0.3 किमी)"
        ),
        "fixed_deposit": lambda user: (
            "**आपकी सावधि जमा**\n\n"
            "| विवरण | जानकारी |\n|---|---|\n"
            "| मूल राशि | ₹ 50,000 |\n"
            "| ब्याज दर | 7.25% प्रति वर्ष |\n"
            "| परिपक्वता तिथि | 15 दिसंबर 2025 |\n"
            "| परिपक्वता राशि | ₹ 53,625 |\n\n"
            "💡 ऑटो-नवीनीकरण सक्षम है।"
        ),
        "fraud": lambda user: (
            "⚠️ **धोखाधड़ी अलर्ट — तत्काल कार्रवाई आवश्यक**\n\n"
            "**साझा न करें:**\n"
            "❌ OTP / PIN\n"
            "❌ CVV / कार्ड नंबर\n\n"
            "**तत्काल कदम:**\n"
            "1. 📞 कॉल करें: **1800-XXX-0001** (24×7)\n"
            "2. 🔒 कार्ड ब्लॉक करें: ऐप → कार्ड → ब्लॉक\n\n"
            "⚡ हम कभी OTP या पासवर्ड नहीं मांगते!"
        ),
        "upi": lambda user: (
            "**UPI भुगतान सेवाएं**\n\n"
            "| सुविधा | जानकारी |\n|---|---|\n"
            "| UPI ID | rajesh@neobank |\n"
            "| दैनिक सीमा | ₹ 1,00,000 |\n"
            "| आज का उपयोग | ₹ 5,450 |\n\n"
            "भुगतान विफल? 30 मिनट में स्वतः वापस होगा।"
        ),
        "interest_rate": lambda user: (
            "**वर्तमान NeoBank ब्याज दरें**\n\n"
            "| उत्पाद | दर |\n|---|---|\n"
            "| बचत खाता | 3.5% प्रति वर्ष |\n"
            "| सावधि जमा (1 वर्ष) | 6.75% प्रति वर्ष |\n"
            "| गृह ऋण | 8.50% प्रति वर्ष |\n"
            "| व्यक्तिगत ऋण | 12.50% प्रति वर्ष |"
        ),
        "thanks": lambda user: f"आपका स्वागत है, {user['full_name'].split()[0]} जी! 😊 क्या आपको और कोई सहायता चाहिए?",
        "bye": lambda user: f"धन्यवाद {user['full_name'].split()[0]} जी! 👋 NeoBank के साथ बैंकिंग के लिए आभार।",
        "unknown": lambda user: (
            "मुझे खेद है, मैं आपका प्रश्न नहीं समझ पाया। 🤔\n\n"
            "कृपया इनके बारे में पूछें:\n"
            "• 💰 खाता शेष\n• 📋 लेनदेन\n• 🏠 ऋण\n"
            "• 💳 क्रेडिट कार्ड\n• 🎧 ग्राहक सेवा"
        ),
    },

    "Telugu": {
        "greeting": lambda user: (
            f"నమస్కారం {user['full_name'].split()[0]} గారూ! 👋 NeoBank AI అసిస్టెంట్‌కి స్వాగతం.\n\n"
            "నేను మీకు సహాయం చేయగలను:\n"
            "• 💰 ఖాతా నిల్వ\n• 📋 లావాదేవీలు\n• 🏠 రుణాలు\n"
            "• 💳 క్రెడిట్ కార్డ్\n• 📈 స్థిర డిపాజిట్లు\n• 🎧 కస్టమర్ సపోర్ట్\n\n"
            "ఈ రోజు నేను మీకు ఎలా సహాయం చేయగలను?"
        ),
        "balance": lambda user: (
            f"**ఖాతా నిల్వ — {_now()}**\n\n"
            f"👤 ఖాతాదారు: {user['full_name']}\n"
            f"🏦 ఖాతా నంబర్: {user['acct_no']}\n\n"
            "| | మొత్తం |\n|---|---|\n"
            "| 💚 అందుబాటులో ఉన్న నిల్వ | ₹ 1,42,580.00 |\n"
            "| 📒 లెడ్జర్ నిల్వ | ₹ 1,45,000.00 |\n"
            "| 🔒 నిరోధించిన మొత్తం | ₹ 2,420.00 |\n\n"
            "✅ ఖాతా స్థితి: **చురుకుగా ఉంది**"
        ),
        "transactions": lambda user: (
            "**ఇటీవలి లావాదేవీలు (గత 10 రోజులు)**\n\n"
            "| తేదీ | వివరణ | మొత్తం | రకం |\n|---|---|---|---|\n"
            "| 28 మే | Swiggy ఆర్డర్ | ₹ 450 | 🔴 డెబిట్ |\n"
            "| 27 మే | UPI చెల్లింపు | ₹ 5,000 | 🔴 డెబిట్ |\n"
            "| 26 మే | జీతం జమ | ₹ 52,000 | 🟢 క్రెడిట్ |\n"
            "| 25 మే | Amazon కొనుగోలు | ₹ 1,299 | 🔴 డెబిట్ |\n"
            "| 24 మే | ATM డబ్బు తీయడం | ₹ 3,000 | 🔴 డెబిట్ |\n\n"
            "📧 పూర్తి స్టేట్‌మెంట్ మీ ఇమెయిల్‌కి పంపబడింది."
        ),
        "loan": lambda user: (
            "**మీ సక్రియ రుణాలు**\n\n"
            "**🏠 గృహ రుణం**\n"
            "| వివరణ | సమాచారం |\n|---|---|\n"
            "| రుణ ID | HL-20219876 |\n"
            "| అసల్ మొత్తం | ₹ 25,00,000 |\n"
            "| చెల్లింపు మొత్తం | ₹ 18,43,200 |\n"
            "| నెలవారీ EMI | ₹ 21,500 |\n"
            "| తదుపరి తేదీ | 5 జూన్ 2025 |\n"
            "| వడ్డీ రేటు | 8.5% వార్షిక |\n\n"
            "💡 *ముందస్తు చెల్లింపు ద్వారా 30% వడ్డీ ఆదా చేయవచ్చు.*"
        ),
        "credit_card": lambda user: (
            "**క్రెడిట్ కార్డ్ సారాంశం**\n\n"
            "💳 **NeoBank Platinum Visa** — ●●●● ●●●● ●●●● 8832\n\n"
            "| వివరణ | విలువ |\n|---|---|\n"
            "| క్రెడిట్ పరిమితి | ₹ 2,00,000 |\n"
            "| వినియోగించింది | ₹ 32,480 |\n"
            "| అందుబాటు క్రెడిట్ | ₹ 1,67,520 |\n"
            "| చెల్లింపు తేదీ | 10 జూన్ 2025 |\n"
            "| రివార్డ్ పాయింట్లు | 4,820 pts |\n\n"
            "⚠️ వడ్డీ నివారించడానికి సకాలంలో చెల్లించండి."
        ),
        "support": lambda user: (
            "**కస్టమర్ సపోర్ట్ — NeoBank**\n\n"
            "| మాధ్యమం | వివరణ |\n|---|---|\n"
            "| 📞 టోల్-ఫ్రీ | 1800-XXX-XXXX (24×7) |\n"
            "| 📧 ఇమెయిల్ | support@neobank.in |\n"
            "| 💬 లైవ్ చాట్ | యాప్‌లో అందుబాటులో |\n\n"
            "సగటు వేచి ఉండే సమయం: **< 2 నిమిషాలు**"
        ),
        "branch": lambda user: (
            "**మీకు సమీపంలో NeoBank శాఖలు**\n\n"
            "| శాఖ | దూరం | సమయాలు |\n|---|---|---|\n"
            "| 📍 బంజారా హిల్స్ | 0.8 కి.మీ | సోమ–శని 9AM–4PM |\n"
            "| 📍 హైటెక్ సిటీ | 2.1 కి.మీ | సోమ–శని 9AM–4PM |\n"
            "| 📍 జూబిలీ హిల్స్ | 3.4 కి.మీ | సోమ–శని 9AM–4PM |\n\n"
            "🏧 **సమీప ATM:** బంజారా హిల్స్ (0.3 కి.మీ)"
        ),
        "fixed_deposit": lambda user: (
            "**మీ స్థిర డిపాజిట్లు**\n\n"
            "| వివరణ | సమాచారం |\n|---|---|\n"
            "| అసల్ మొత్తం | ₹ 50,000 |\n"
            "| వడ్డీ రేటు | 7.25% వార్షిక |\n"
            "| మెచ్యూరిటీ తేదీ | 15 డిసెంబర్ 2025 |\n"
            "| మెచ్యూరిటీ విలువ | ₹ 53,625 |\n\n"
            "💡 ఆటో-రివ్యూవల్ ప్రారంభించబడింది."
        ),
        "fraud": lambda user: (
            "⚠️ **మోసం హెచ్చరిక — వెంటనే చర్య తీసుకోండి**\n\n"
            "**షేర్ చేయవద్దు:**\n"
            "❌ OTP / PIN\n"
            "❌ CVV / కార్డ్ నంబర్\n\n"
            "**వెంటనే చేయవలసినవి:**\n"
            "1. 📞 కాల్ చేయండి: **1800-XXX-0001** (24×7)\n"
            "2. 🔒 కార్డ్ బ్లాక్ చేయండి: యాప్ → కార్డ్స్ → బ్లాక్\n\n"
            "⚡ మేము OTP లేదా పాస్‌వర్డ్ ఎప్పుడూ అడగం!"
        ),
        "upi": lambda user: (
            "**UPI చెల్లింపు సేవలు**\n\n"
            "| సువిధ | సమాచారం |\n|---|---|\n"
            "| UPI ID | rajesh@neobank |\n"
            "| రోజువారీ పరిమితి | ₹ 1,00,000 |\n"
            "| నేడు వాడిన మొత్తం | ₹ 5,450 |\n\n"
            "చెల్లింపు విఫలమైందా? 30 నిమిషాల్లో స్వయంచాలకంగా వాపసు అవుతుంది."
        ),
        "interest_rate": lambda user: (
            "**ప్రస్తుత NeoBank వడ్డీ రేట్లు**\n\n"
            "| ఉత్పత్తి | రేటు |\n|---|---|\n"
            "| సేవింగ్స్ అకౌంట్ | 3.5% వార్షిక |\n"
            "| స్థిర డిపాజిట్ (1 సం.) | 6.75% వార్షిక |\n"
            "| గృహ రుణం | 8.50% వార్షిక |\n"
            "| వ్యక్తిగత రుణం | 12.50% వార్షిక |"
        ),
        "thanks": lambda user: f"మీకు స్వాగతం, {user['full_name'].split()[0]} గారూ! 😊 మరేమైనా సహాయం అవసరమా?",
        "bye": lambda user: f"వీడ్కోలు {user['full_name'].split()[0]} గారూ! 👋 NeoBank తో బ్యాంకింగ్ చేసినందుకు ధన్యవాదాలు.",
        "unknown": lambda user: (
            "క్షమించండి, మీ ప్రశ్న అర్థం కాలేదు. 🤔\n\n"
            "దయచేసి ఇవి అడగండి:\n"
            "• 💰 ఖాతా నిల్వ\n• 📋 లావాదేవీలు\n• 🏠 రుణాలు\n"
            "• 💳 క్రెడిట్ కార్డ్\n• 🎧 కస్టమర్ సపోర్ట్"
        ),
    }
}


def get_response(user_text: str, user: dict, language: str = "English") -> str:
    """Main entry point: detect intent, return localised response."""
    intent = detect_intent(user_text)
    lang_responses = RESPONSES.get(language, RESPONSES["English"])
    handler = lang_responses.get(intent, lang_responses["unknown"])
    return handler(user)
