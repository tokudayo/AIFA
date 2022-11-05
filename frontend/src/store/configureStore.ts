import { createStore, applyMiddleware } from 'redux';
import createSagaMiddleware from 'redux-saga'
import rootReducer from "./reducers";

function configureStore() {
  // Note: passing middleware as the last argument to createStore requires redux@>=3.1.0
  const sagaMiddleware = createSagaMiddleware()
  return {
    ...createStore(rootReducer, {}, applyMiddleware(sagaMiddleware)),
    runSaga: sagaMiddleware.run
  }
}
const store = configureStore();
export default store;
