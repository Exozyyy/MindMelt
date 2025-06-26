import { configureStore } from "@reduxjs/toolkit";
import type { Action, ThunkAction} from "@reduxjs/toolkit";
import {type TypedUseSelectorHook, useSelector} from "react-redux";
import topicReducer from "./topicSlice";


export const store = configureStore({
    reducer: {
        topic: topicReducer,

    }
})


export type AppStore = typeof store
export type RootState = ReturnType<AppStore['getState']>
export type AppDispatch = AppStore['dispatch']
export type AppThunk<ThunkReturnType = void> = ThunkAction<
    ThunkReturnType,
    RootState,
    unknown,
    Action
>

export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector
export const useAppDispatch = () => store.dispatch as AppDispatch
export const useAppStore = () => store as AppStore