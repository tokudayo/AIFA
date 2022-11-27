import "antd/dist/antd.min.css";
import styles from "./Layout.module.css";
import {
  AlignLeftOutlined,
  CameraOutlined,
  LogoutOutlined,
  VideoCameraOutlined,
} from "@ant-design/icons";
import { Alert, Layout as LayoutAnt, Menu } from "antd";
import React, { useEffect, useState } from "react";
import { useNavigate, Outlet, useLocation } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { getLoginStorage, logout } from "../../store/auth/actions";
import { RootState } from "../../store/reducers";
import eventBus from "../../event/event-bus";
import { SocketEvent } from "../../socket/SocketEvent";
const { Content, Sider } = LayoutAnt;

const Layout = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => state.AuthReducer);
  const [alert, setAlert] = useState("Ready");

  useEffect(() => {
    dispatch(getLoginStorage());
  }, [dispatch]);

  useEffect(() => {
    let timeout = setTimeout(() => setAlert("Ready"), 1500);

    eventBus.on(SocketEvent.ALERT, async (data: string) => {
      clearTimeout(timeout);
      timeout = setTimeout(() => setAlert("Ready"), 1500);
      if (data.trim().length === 0) {
        setAlert("Correct");
      } else {
        setAlert(data);
      }
    });
  }, []);

  useEffect(() => {
    if (user === null) {
      navigate("/");
    }
  }, [user, navigate]);

  return (
    <LayoutAnt style={{ height: "100vh" }}>
      <Sider breakpoint="lg" collapsedWidth="0">
        <div style={{ padding: "16px" }}>
          <div className={styles.logo} />
          <p style={{ color: "white", marginTop: "10px" }}>
            AIFA - Realtime posture correction
          </p>
        </div>
        <Menu
          theme="dark"
          mode="inline"
          onClick={(e) => {
            if (e.key === "1") {
              navigate("/index");
            } else if (e.key === "2") {
              navigate("/index/camera");
            } else if (e.key === "3") {
              navigate("/index/history");
            } else if (e.key === "4") {
              dispatch(logout());
            }
          }}
          defaultSelectedKeys={["1"]}
          selectedKeys={[
            location.pathname.includes("camera")
              ? "2"
              : location.pathname.includes("analytics")
              ? "3"
              : "1",
          ]}
          items={[
            {
              icon: CameraOutlined,
              label: "Webcam Streaming",
            },
            {
              icon: VideoCameraOutlined,
              label: "Camera Streaming",
            },
            {
              icon: AlignLeftOutlined,
              label: "History",
            },
            {
              icon: LogoutOutlined,
              label: "Logout",
            },
          ].map((item, index) => ({
            key: String(index + 1),
            icon: React.createElement(item.icon),
            label: item.label,
          }))}
        />
      </Sider>
      <LayoutAnt>
        {/* <Header
          className={styles["site-layout-sub-header-background"]}
          style={{
            padding: 0,
          }}
        /> */}
        <Content
          style={{
            margin: "10px 16px 0",
          }}
        >
          <div
            className={styles["site-layout-background"]}
            style={{
              padding: 5,
              minHeight: 360,
              position: "relative",
            }}
          >
            <>
              {!location.pathname.includes("analytics") && (
                <>
                  {alert === "Ready" && (
                    <Alert
                      message={alert}
                      type="warning"
                      className={`${styles.alert}`}
                    />
                  )}
                  {alert === "Correct" && (
                    <Alert
                      message={alert}
                      type="success"
                      className={`${styles.alert}`}
                    />
                  )}
                  {alert !== "Correct" && alert !== "Ready" && (
                    <Alert
                      message={alert}
                      type="error"
                      className={`${styles.alert}`}
                    />
                  )}
                </>
              )}
            </>
            <Outlet />
          </div>
        </Content>
      </LayoutAnt>
    </LayoutAnt>
  );
};

export default Layout;
