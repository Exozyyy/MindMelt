import {useState} from "react";
const Topic = () => {
    const [topic, setTopic] = useState<string>("");
    return (
        <div className="topic-container">
            <h2 className="text-2xl font-bold mb-4">Введите тему, в которой хотите разобраться</h2>
            <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="Хочу разобраться с.."
                className="border p-2 w-full"
            />
            <br/>
            <button>Узнать про {topic}</button>
        </div>
    )
}
export default Topic;