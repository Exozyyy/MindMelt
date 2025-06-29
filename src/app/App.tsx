
import '../App.css'
import Header from "../shared/ui/Header.tsx";
import Topic from "../entities/topic/ui/Topic.tsx";
import ExplanationView from "../pages/QuizPage/ExplanationView.tsx";


function App() {
  return (
    <>
        <Header />
        <Topic />
        <ExplanationView />

    </>
  )
}

export default App
