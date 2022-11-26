import { Card } from "antd";
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getAnalytics } from "../../store/analytics/actions";
import { RootState } from "../../store/reducers";

export default function Analytics() {
  const dispatch = useDispatch();
  const { loading, analytics, error } = useSelector(
    (state: RootState) => state.AnalyticReducer
  );

  useEffect(() => {
    if (!loading && !analytics && !error.message.length) {
      dispatch(getAnalytics());
    }
  }, [dispatch, loading, error, analytics]);

  return (
    <>
      {(analytics || []).map((analytic) => (
        <Card
          key={analytic.id}
          title={analytic.exercise}
          bordered={true}
          style={{ width: 300 }}
        >
          <p>Platform: {analytic.platform}</p>
          <p>Correct: {analytic.correct}</p>
          <p>Start Time: {analytic.startTime}</p>
          <p>End Time: {analytic.endTime}</p>
        </Card>
      ))}
    </>
  );
}
