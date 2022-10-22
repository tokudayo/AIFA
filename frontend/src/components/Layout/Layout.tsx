import "antd/dist/antd.min.css";
import styles from "./Layout.module.css";
import {
  UploadOutlined,
  UserOutlined,
  CameraOutlined,
  VideoCameraOutlined,
} from "@ant-design/icons";
import { Layout as LayoutAnt, Menu } from "antd";
import React from "react";
import { useNavigate, Outlet } from "react-router-dom";
const { Header, Content, Footer, Sider } = LayoutAnt;

const Layout = () => {
  const navigate = useNavigate();

  return (
    <LayoutAnt style={{ height: "100vh" }}>
      <Sider breakpoint="lg" collapsedWidth="0">
        <div className={styles.logo} style={{ marginBottom: '50px', marginTop: '20px' }} />
        <Menu
          theme="dark"
          mode="inline"
          onClick={(e) => {
            if (e.key === "1") {
              navigate("/index");
            } else if (e.key === "2") {
              navigate("/index/camera");
            } else {
              navigate("/dmm");
            }
          }}
          defaultSelectedKeys={["1"]}
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
              icon: UploadOutlined,
              label: "Upload Image",
            },
            { icon: UserOutlined, label: "User Information" },
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
