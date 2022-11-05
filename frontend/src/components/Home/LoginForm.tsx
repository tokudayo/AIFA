import { FormEvent, useCallback, useState } from "react";
import { Button, Form, Card, Spinner } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { login } from "../../store/auth/actions";
import { RootState } from "../../store/reducers";
import styles from "./LoginForm.module.css";

export default function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const dispatch = useDispatch();
  const { loading } = useSelector((state: RootState) => state.AuthReducer);

  const handleLogin = useCallback(
    (e: FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      dispatch(login({ email, password }));
    },
    [email, password, dispatch]
  );

  return (
    <div className={styles.loginContainer}>
      <div className="col-sm-10 col-md-8 col-lg-6 col-xl-4">
        <Card>
          <Card.Body className="p-5">
            <Form onSubmit={handleLogin}>
              <Form.Group className="mb-3" controlId="formBasicEmail">
                <Form.Control
                  size="lg"
                  type="email"
                  placeholder="Email"
                  value={email}
                  onChange={(e) => setEmail(e.currentTarget.value)}
                />
              </Form.Group>

              <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Control
                  size="lg"
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.currentTarget.value)}
                />
              </Form.Group>
              <div className="d-grid gap-2 mb-3">
                <Button size="lg" variant="primary" type="submit">
                  {loading && (
                    <Spinner
                      as="span"
                      animation="grow"
                      size="sm"
                      role="status"
                      aria-hidden="true"
                    />
                  )}
                  Login
                </Button>
              </div>
              <div style={{ display: "flex" }}>
                <p style={{ fontSize: 15 }}>
                  If you don't have an account. Please sign up&nbsp;
                </p>
                <a style={{ fontSize: 15 }} href="/sign_up">
                  here
                </a>
              </div>
            </Form>
          </Card.Body>
        </Card>
      </div>
    </div>
  );
}
