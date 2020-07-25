import React from "react";
import { Button, Row, Col } from "antd";
import {
  SearchOutlined,
  TeamOutlined,
  MessageOutlined,
  TwitterOutlined,
} from "@ant-design/icons";

const showModal = (option) => {
  console.log("option ==>", option);
};

const Auth = () => {
  return (
    <Row>
      <Col span={12}>
        <h2>
          <SearchOutlined /> Follow your interests.
        </h2>
        <h2>
          <TeamOutlined /> Hear what people are talking about.
        </h2>
        <h2>
          <MessageOutlined /> Join the conversation.
        </h2>
      </Col>
      <Col span={12}>
        <h1>
          <TwitterOutlined />
          <br />
          See what’s happening in the world right now
        </h1>
        <br />
        <br />
        <h4>Join Twitter today.</h4>
        <Button type="primary" shape="round" block onClick={() => showModal("signup")}>
          Sign up
        </Button>
        <Button shape="round" onClick={() => showModal("login")}>
          Log in
        </Button>
      </Col>
    </Row>
  );
};

export default Auth;
