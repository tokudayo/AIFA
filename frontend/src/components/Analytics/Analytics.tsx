import { Card } from "antd";
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getAnalytics } from "../../store/analytics/actions";
import { RootState } from "../../store/reducers";

const sumValues = (obj: object) =>
  Object.values(obj).reduce((a: number, b: number) => a + b, 0);

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
          title={
            analytic.exercise === "shoulder_press"
              ? "Shoulder Press"
              : analytic.exercise === "deadlift"
              ? "Deadlift"
              : "Hammer Curl"
          }
          bordered={true}
          style={{ width: 300 }}
        >
          <p>Platform: {analytic.platform === "web" ? "Web" : "Android"}</p>
          <p>
            Correct: {(analytic.count as any).Correct || 0}/
            {sumValues(analytic.count)}
          </p>
          <p>Start Time: {new Date(analytic.startTime).toLocaleString()}</p>
          <p>End Time: {new Date(analytic.endTime).toLocaleString()}</p>
        </Card>
      ))}
    </>
  );
}
