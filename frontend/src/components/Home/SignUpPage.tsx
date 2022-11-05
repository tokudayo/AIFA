import { Col, Row } from "antd";
import styles from "./SignUpPage.module.css";
import SignUpForm from "./SignUpForm";
import { useDispatch, useSelector } from "react-redux";
import { RootState } from "../../store/reducers";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { clearSuccessSignUp } from "../../store/auth/actions";

const SignUpPage = () => {
  const { signUpSuccess } = useSelector((state: RootState) => state.AuthReducer);
  const dispatch = useDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    dispatch(clearSuccessSignUp());
  }, [dispatch])

  useEffect(() => {
    if (signUpSuccess) {
      navigate("/");
    }
  }, [signUpSuccess, navigate])

  return (
    <Row className={styles.background} justify="center" align="middle">
      <Col>
        <SignUpForm />
      </Col>
    </Row>
  );
};

export default SignUpPage;
