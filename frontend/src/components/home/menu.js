import React from "react";
import { Menu } from "antd";
import {
  HomeOutlined,
  BellOutlined,
  MailOutlined,
  BookOutlined,
  UserOutlined,
} from "@ant-design/icons";
import { BrowserRouter as Router, Switch, Route, Link } from "react-router-dom";

import Home from "./index";
import Notifications from "./../profile/notifications";

const SideMenu = () => {
  return (
    <div className="menu">
      <img
        width={41}
        alt="logo"
        src="https://res.cloudinary.com/kwangonya/image/upload/v1595672474/witter/Twitter_bird_logo_2012.svg.png"
      />
      <Router>
        <Menu
          style={{ width: 256 }}
          defaultSelectedKeys={["home_menu"]}
          mode="inline"
        >
          <Menu.Item icon={<HomeOutlined />} key="home_menu">
            Home
            <Link to="/"/>
          </Menu.Item>
          <Menu.Item icon={<BellOutlined />} key="notifications_menu">
            Notifications
            <Link to="/notifications"/>
          </Menu.Item>
          <Menu.Item icon={<MailOutlined />} key="messages_menu">
            Messages
            <Link to="/messages"/>
          </Menu.Item>
          <Menu.Item icon={<BookOutlined />} key="bookmarks_menu">
            Bookmarks
            <Link to="/bookmarks"/>
          </Menu.Item>
          <Menu.Item icon={<UserOutlined />} key="profile_menu">
            Profile
            <Link to="/profile"/>
          </Menu.Item>
        </Menu>
        <Switch>
          <Route path="/notifications">
            <Notifications />
          </Route>
        </Switch>
      </Router>
    </div>
  );
};

export default SideMenu;
