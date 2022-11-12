import { FormEvent, useCallback, useState } from "react";
import { Button, Form, Card, Spinner } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { signUp } from "../../store/auth/actions";
import { RootState } from "../../store/reducers";
import styles from "./SignUpForm.module.css";

export default function SignUpForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [passwordConfirmation, setPasswordConfirmation] = useState("");
  const dispatch = useDispatch();
  const { loading } = useSelector((state: RootState) => state.AuthReducer);

  const handleSignUp = useCallback(
    (e: FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      dispatch(signUp({ email, password, passwordConfirmation }));
    },
    [email, password, passwordConfirmation, dispatch]
  );

  return (
    <div className={styles.loginContainer}>
      <div className="col-sm-10 col-md-8 col-lg-6 col-xl-4">
        <Card>
          <Card.Body className="p-5">
            <Form onSubmit={handleSignUp}>
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
              <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Control
                  size="lg"
                  type="password"
                  placeholder="Password Confirmation"
                  value={passwordConfirmation}
                  onChange={(e) =>
                    setPasswordConfirmation(e.currentTarget.value)
                  }
                />
              </Form.Group>
              <div className="d-grid gap-2 mt-4">
                <Button size="lg" variant="warning" type="submit">
                  {loading && (
                    <Spinner
                      as="span"
                      animation="grow"
                      size="sm"
                      role="status"
                      aria-hidden="true"
                    />
                  )}
                  &nbsp;Sign Up
                </Button>
              </div>
            </Form>
          </Card.Body>
        </Card>
      </div>
    </div>
  );
}
