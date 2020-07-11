package com.df.bbt.service;

import com.alibaba.fastjson.JSONObject;
import com.df.bbt.entity.User;
import com.df.bbt.mapper.PriceMapper;
import com.df.bbt.mapper.UserMapper;
import com.sun.org.apache.regexp.internal.RE;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.JwtBuilder;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import javax.sound.sampled.Line;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;
import java.util.logging.Logger;

/**
 * @author Lin
 * @create 2020/4/28
 * @since 1.0.0
 * (功能)：判断登录信息状态的服务层
 */
@Slf4j
@Service
public class LoginService {

    @Autowired
    UserMapper userMapper;

    @Autowired
    PriceMapper priceMapper;

    //根据token判断用户登录信息
    public JSONObject judgeLogin(String token){
       JSONObject jsonObject = new JSONObject();
       String status;
       try {
           Claims claims = Jwts.parser().setSigningKey("itcast").parseClaimsJws(token).getBody();
           String userName = claims.getSubject();
           status = "200";
           log.info(userName + "用户登录成功");
           jsonObject.put("status", status);
           jsonObject.put("userName", userName);
       }catch (Exception e){
           status="500";
           log.info("登录失败");
           jsonObject.put("status", status);
           jsonObject.put("userName",null);
       }
       return jsonObject;
    }

    //进行登录操作
    public JSONObject login(User user){
        String token;
        String name = userMapper.getName(user);
        Map<String, String> content = new HashMap<>();
        if (name != null){
            content.put("name", name);
            content.put("status", "200");
        }else {
            content.put("status", "500");
        }
        token = judgeLoginToken(content, user);


        JSONObject result = new JSONObject();
        result.put("status", content.get("status"));
        result.put("token", token);

        return result;
    }

    public String judgeLoginToken(Map<String, String> content, User user){
        String token;
        if(content.get("status").equals("200")) {
            //判定成功后整合成token签名转发回去
            JwtBuilder jwtBuilder = Jwts.builder();
            jwtBuilder.setId(user.getUserAccount()); //id
            jwtBuilder.setSubject(content.get("name"));	//名字
            jwtBuilder.setIssuedAt(new Date()); //登录时间
            jwtBuilder.signWith(SignatureAlgorithm.HS256, "itcast"); //头部信息 第一个参数为加密方式为哈希 256  第二个参数为加的盐(key)为itcast
            jwtBuilder.setExpiration(new Date(new Date().getTime()+60000000));//设置token 的过期时间为十分钟
            jwtBuilder.claim("role", "user");
            token = jwtBuilder.compact();
        }else {
            log.info("登录失败，账号或密码错误");
            token = null;
        }
        return token;
    }



    //判断账号是否已经被注册
    public JSONObject judgeAccount(String account) {
        log.info("判断" + account + "是否被注册");
        int judgeResult = userMapper.judgeAccount(account);
        JSONObject jsonObject = new JSONObject();
        jsonObject.put("status",judgeResult==0?200:500);
        if (judgeResult == 0) log.info(account+"没有被注册");
        else log.info(account+"已经被注册");
        return jsonObject;
    }

    //注册功能
    public JSONObject regist(User user){
        log.info("开始注册："+user.getUserAccount());
        int num = userMapper.registUser(user);
        JSONObject result = new JSONObject();
        result.put("rows",num);
        if (num == 0) log.info("注册失败："+user.getUserAccount());
        else log.info("注册成功："+user.getUserAccount());
        return result;
    }

    //通过token 获取account
    public JSONObject getAccount(String token) {
        String userAccount;
        try {
            Claims claims = Jwts.parser().setSigningKey("itcast")
                    .parseClaimsJws(token)
                    .getBody();
            userAccount = claims.getId();
        }catch (Exception e) {
            userAccount=null;
        }
        JSONObject result = new JSONObject();
        result.put("userAccount", userAccount);
        return result;
    }

    //通过token获取用户信息
    public JSONObject getUser(String token) { ;
        JSONObject jsonObject = new JSONObject();
        String userAccount;
        try {
            Claims claims = Jwts.parser().setSigningKey("itcast")
                    .parseClaimsJws(token)
                    .getBody();
            userAccount = claims.getId();
        }catch (Exception e) {
            userAccount=null;
            jsonObject.put("Account", userAccount);
            log.info("获取个人信息失败,需要重新登录！");
            return jsonObject;
        }
        log.info("开始获取"+userAccount+"的个人信息");
        Integer userId = priceMapper.getUserIdPassAcc(userAccount);
        User user = userMapper.getUserById(userId);
        jsonObject = dealUserDetail(user);
        log.info("成功获取"+userAccount+"的个人信息");
        return jsonObject;
    }

    //根据返回的user信息 包装成JSONOBJECT
    public JSONObject dealUserDetail(User user){
        JSONObject result =new JSONObject();
        result.put("userAccount", user.getUserAccount());
        result.put("userName", user.getUserName());
        result.put("gender", user.getGender());
        result.put("marital", user.getMaritalStatus());
        result.put("level", user.getLevel());
        result.put("tel", user.getPhoneNumber());
        result.put("Email", user.getEMail());
        return result;
    }

    //替换user的内容
    public JSONObject preserveUser(User user) {
        log.info("开始修改"+user.getUserAccount()+"的个人信息");
        int status = userMapper.updateUser(user);
        Map<String, String> map = new HashMap<>();
        if (status == 0){
            status = 500;
            map.put("status","500");
        }else {
            status = 200;
            map.put("status","200");
            map.put("name", user.getUserName());
        }
        String token = judgeLoginToken(map, user);
        JSONObject jsonObject = new JSONObject();
        log.info("成功修改"+user.getUserAccount()+"的个人信息");
        jsonObject.put("status",status);
        jsonObject.put("token", token);
        return jsonObject;
    }
}
