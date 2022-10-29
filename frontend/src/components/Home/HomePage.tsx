import { Button, Col, Row } from "antd";
import styles from "./HomePage.module.css";

const HomePage = () => {
  return (
    <Row className={styles.background} justify="center" align="middle">
      <Col>
        <Button type="primary" className={styles.button} href="/index">GET STARTED</Button>
      </Col>
    </Row>
  );
};

export default HomePage;
