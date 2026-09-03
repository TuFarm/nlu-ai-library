import { KioskChrome } from "../../components/kiosk/KioskChrome";
import { useKioskFlow } from "../../hooks/useKioskFlow";
import FaceScanningScreen from "./FaceScanningScreen";
import FaceUnknownScreen from "./FaceUnknownScreen";
import KioskBookSuggestionScreen from "./KioskBookSuggestionScreen";
import KioskChatScreen from "./KioskChatScreen";
import KioskErrorScreen from "./KioskErrorScreen";
import KioskIdleScreen from "./KioskIdleScreen";
import KioskSurveyScreen from "./KioskSurveyScreen";
import KioskThankYouScreen from "./KioskThankYouScreen";
import WelcomeScreen from "./WelcomeScreen";

export default function KioskApp(){const flow=useKioskFlow();const content=(()=>{switch(flow.currentState){case"IDLE":return <KioskIdleScreen onStart={flow.startMockPresence}/>;case"PRESENCE_DETECTED":return <div className="kiosk-center"><div className="state-symbol success">◎</div><h1>Đã phát hiện người dùng</h1><p>Đang chuẩn bị nhận diện...</p></div>;case"FACE_SCANNING":return <FaceScanningScreen onSuccess={flow.handleMockFaceSuccess} onUnknown={flow.handleMockFaceUnknown}/>;case"FACE_RECOGNIZED":return <div className="kiosk-center"><div className="state-symbol success">✓</div><h1>Đã nhận diện thành công</h1></div>;case"WELCOME":return <WelcomeScreen user={flow.currentUser} onContinue={flow.startChat}/>;case"FACE_UNKNOWN":return <FaceUnknownScreen onRetry={()=>flow.transitionTo("FACE_SCANNING")} onGuest={flow.startChat}/>;case"AI_CHAT":return <KioskChatScreen name={flow.currentUser?.full_name} onBooks={()=>flow.transitionTo("BOOK_SUGGESTION")} onSurvey={flow.startSurvey}/>;case"BOOK_SUGGESTION":return <KioskBookSuggestionScreen onBack={flow.startChat} onSurvey={flow.startSurvey}/>;case"SURVEY":return <KioskSurveyScreen onComplete={flow.completeSurvey}/>;case"THANK_YOU":return <KioskThankYouScreen onHome={flow.resetToIdle}/>;default:return <KioskErrorScreen onRetry={()=>flow.transitionTo("FACE_SCANNING")} onHome={flow.resetToIdle}/>}})();return <KioskChrome state={flow.currentState} onExit={flow.currentState!=="IDLE"?flow.resetToIdle:undefined}>{content}</KioskChrome>}
