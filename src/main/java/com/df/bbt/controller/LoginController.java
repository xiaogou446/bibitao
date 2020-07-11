package com.df.bbt.controller;

import com.alibaba.fastjson.JSONObject;
import com.df.bbt.entity.User;
import com.df.bbt.service.LoginService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * @author Lin
 * @create 2020/4/28
 * @since 1.0.0
 * (功能)：一个操作登录及判断相关的Controller
 */
@Slf4j
@RestController
public class LoginController {

    @Autowired
    LoginService loginService;

    //判断用户登录状态
    @PostMapping(value = "/judgeLoginStatus.action", produces = "application/json;charset=utf-8")
    public String judgeLoginStatus(@RequestBody JSONObject jsonObject){
        String token = (String) jsonObject.get("token");
        JSONObject result = loginService.judgeLogin(token);
        return result.toJSONString();
    }

    //进行登录
    @PostMapping(value = "/login.action", produces = "application/json;charset=utf-8")
    public String login(@RequestBody JSONObject jsonObject){
        User user = new User();
        user.setUserAccount((String) jsonObject.get("account"));
        log.info((String) jsonObject.get("account")+"开始登录");
        user.setUserPassword((String) jsonObject.get("password"));
        JSONObject result = loginService.login(user);
        return result.toJSONString();
    }

    //判定注册账号是否存在
    @PostMapping(value = "/judgeAccount.action", produces = "application/json;charset=utf-8")
    public String judgeAccount(@RequestBody JSONObject jsonObject){
        JSONObject result = loginService.judgeAccount((String) jsonObject.get("account"));
        return result.toJSONString();
    }

    //进行注册
    @PostMapping(value = "/regist.action", produces = "application/json;charset=utf-8")
    public String regist(@RequestBody JSONObject jsonObject){
        User user = new User();
        user.setUserAccount((String) jsonObject.get("account"));
        user.setUserName((String) jsonObject.get("name"));
        user.setUserPassword((String) jsonObject.get("password"));
        user.setEMail((String) jsonObject.get("Email"));
        user.setPhoneNumber((String) jsonObject.get("tel"));
        JSONObject result = loginService.regist(user);
        return result.toJSONString();
    }

    //根据token获取账号信息
    @PostMapping(value = "/getAccount.action", produces = "application/json;charset=utf-8")
    public String getAccount(@RequestBody JSONObject jsonObject){
        String token = (String) jsonObject.get("token");
        JSONObject account = loginService.getAccount(token);
        return account.toJSONString();
    }

    //根据token信息获取用户的信息
    @PostMapping(value = "/getUser.action", produces =  "application/json;charset=utf-8")
    public String getUser(@RequestBody JSONObject jsonObject){
        String token = (String) jsonObject.get("token");
        JSONObject user = loginService.getUser(token);
        return user.toJSONString();
    }

    //保存user信息
    @PostMapping(value = "/updateUser.action", produces = "application/json;charset=utf-8")
    public String preserveUser(@RequestBody JSONObject jsonObject){
        User user = new User();
        user.setUserAccount((String) jsonObject.get("userAccount"));
        user.setUserName((String) jsonObject.get("userName"));
        user.setPhoneNumber((String) jsonObject.get("tel"));
        user.setGender((String) jsonObject.get("gender"));
        user.setMaritalStatus((String) jsonObject.get("marital"));
        JSONObject result = loginService.preserveUser(user);
        return result.toJSONString();

    }
}
