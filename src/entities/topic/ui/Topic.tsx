import {setTopic, clearTopic, fetchTopic} from "../model/topicSlice.tsx";
import { useAppDispatch, useAppSelector } from "../../../shared/lib/hooks/Hooks.tsx";
import * as React from "react";


const Topic = () => {
    const dispatch = useAppDispatch();
    const topic = useAppSelector((state) => state.topic.value);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        dispatch(setTopic(e.target.value));
    }
    const handleClick = () => {
        dispatch(fetchTopic(topic));
        dispatch(clearTopic());
    }
    return (
        <div className="topic-container">
            <h2 className="text-2xl font-bold mb-4">Введите тему, в которой хотите разобраться</h2>
            <input
                type="text"
                value={topic}
                onChange={handleChange}
                placeholder="Хочу разобраться с.."
                className="border p-2 w-full"
            />
            <br/>
            <button onClick={handleClick}>Узнать про {topic}</button>
        </div>
    )
}
export default Topic;