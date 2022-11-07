import "antd/dist/antd.min.css";
import styles from "./Layout.module.css";
import {
  CameraOutlined,
  LogoutOutlined,
  VideoCameraOutlined,
} from "@ant-design/icons";
import { Layout as LayoutAnt, Menu } from "antd";
import React, { useEffect } from "react";
import { useNavigate, Outlet, useLocation } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { logout } from "../../store/auth/actions";
import { RootState } from "../../store/reducers";
const { Header, Content, Footer, Sider } = LayoutAnt;

const Layout = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => state.AuthReducer);

  useEffect(() => {
    if (!user) {
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
              dispatch(logout());
            }
          }}
          defaultSelectedKeys={["1"]}
          selectedKeys={[location.pathname.includes("camera") ? "2" : "1"]}
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
        <Header
          className={styles["site-layout-sub-header-background"]}
          style={{
            padding: 0,
          }}
        />
        <Content
          style={{
            margin: "24px 16px 0",
          }}
        >
          <div
            className={styles["site-layout-background"]}
            style={{
              padding: 24,
              minHeight: 360,
            }}
          >
            <Outlet />
          </div>
        </Content>
        <Footer
          style={{
            textAlign: "center",
          }}
        >
          Capstone ©2022 Created by Group 7
        </Footer>
      </LayoutAnt>
    </LayoutAnt>
  );
};

export default Layout;
