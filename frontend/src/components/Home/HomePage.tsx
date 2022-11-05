import { Col, Row } from "antd";
import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import { getLoginStorage } from "../../store/auth/actions";
import { RootState } from "../../store/reducers";
import styles from "./HomePage.module.css";
import LoginForm from "./LoginForm";

const HomePage = () => {
  const { user } = useSelector((state: RootState) => state.AuthReducer);
  const navigate = useNavigate();
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(getLoginStorage());
  }, [dispatch]);

  useEffect(() => {
    if (user) {
      navigate("/index");
    }
  }, [user, navigate]);

  return (
    <Row className={styles.background} justify="center" align="middle">
      <Col>
        <LoginForm />
      </Col>
    </Row>
  );
};

export default HomePage;
