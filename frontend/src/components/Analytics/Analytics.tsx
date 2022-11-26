import { Card, Col, Row } from "antd";
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { getAnalytics } from "../../store/analytics/actions";
import { RootState } from "../../store/reducers";

export default function Analytics() {
  const dispatch = useDispatch();
  const { analytics } = useSelector(
    (state: RootState) => state.AnalyticReducer
  );

  useEffect(() => {
    dispatch(getAnalytics());
  }, [dispatch]);

  return (
    <div style={{ padding: 20 }}>
      <Row gutter={{ xs: 8, sm: 16, md: 24, lg: 32 }}>
        {(analytics || []).map((analytic) => (
          <Col className="gutter-row" span={6}>
            <Card
              key={analytic.id}
              title={analytic.exercise}
              bordered={true}
              style={{ width: 300, marginBottom: 30 }}
            >
              <p>Platform: {analytic.platform}</p>
              <p>Correct: {analytic.correct}</p>
              <p>Start Time: {analytic.startTime}</p>
              <p>End Time: {analytic.endTime}</p>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
}
