import React from "react";
import { Row, Col } from "antd";

import Menu from "./menu"

const Home = () => {
  return (
    <Row>
      <Col flex={3}>
        <Menu />
      </Col>
      <Col flex={5}>center</Col>
      <Col flex={3}>right</Col>
    </Row>
  );
};

export default Home;
