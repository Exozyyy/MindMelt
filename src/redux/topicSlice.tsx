import {createSlice, PayloadAction } from "@reduxjs/toolkit";

interface TopicState {
    value: string;
}

const initialState: TopicState = {
    value: "",
}

const topicSlice = createSlice({
    name: "topic",
    initialState,
    reducers: {
        setTopic: (state, action: PayloadAction<string>) => {
            state.value = action.payload;
        },
        clearTopic: (state) => {
            state.value = "";
        }
    }
})

export const { setTopic, clearTopic } = topicSlice.actions;
export default topicSlice.reducer;