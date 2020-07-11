package com.df.bbt.controller;

import com.alibaba.fastjson.JSONObject;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.util.Map;

/**
 * @author Lin
 * @create 2020/4/27
 * @since 1.0.0
 * (功能)：
 */
@RestController
public class hello {
    //, produces = {"application/json;charset=utf-8"}  Map<String, Object> map  @RequestBody 是封装对象才用
//    @PostMapping(value = "/login.action", produces = "application/json;charset=utf-8")
//    public String login(@RequestBody Map<String, Object> map)  {
//        System.out.println("进来了");
//
////        String a = URLDecoder.decode(s, "utf-8");
////        System.out.println(a);
//        String account = (String) map.get("account");
//        String password = (String) map.get("password");
//        System.out.println(account);
//        System.out.println(password);
//        JSONObject jsonObject = new JSONObject();
//        jsonObject.put("status",200);
//        return jsonObject.toJSONString();
//    }

    @RequestMapping(value = "/hello")
    public String hello(){
        return "hello BBT";
    }

}
