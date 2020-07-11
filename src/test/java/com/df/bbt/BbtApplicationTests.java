package com.df.bbt;


import cn.hutool.core.date.DateUtil;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import javax.sql.DataSource;
import java.sql.Connection;
import java.sql.SQLException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

import static org.assertj.core.util.DateUtil.*;

@SpringBootTest
class BbtApplicationTests {

    @Autowired
    DataSource dataSource;

    @Test
    void contextLoads() throws SQLException {
        System.out.println(dataSource);
        Connection connection = dataSource.getConnection();
        System.out.println(connection);
    }
    @Test
    void test01(){
        String test = "龙湖天街";
        String s = dealDimContent(test);
        System.out.println(s);
    }
    public static String dealDimContent(String content){
        StringBuffer stringBuffer = new StringBuffer();
        for (int i = 0; i < content.length(); i++) {
            stringBuffer.append("%");
            stringBuffer.append(content.charAt(i));
        }
        stringBuffer.append("%");
        return stringBuffer.toString();
    }

    @Test
    void test02(){
        Date date = new Date();
        String year = DateUtil.formatChineseDate(date,true).substring(0,4);
        SimpleDateFormat dateFormat= new SimpleDateFormat("dd-MMM-yyyy", Locale.ENGLISH);
        String browseTime =dateFormat.format(date);
        browseTime = browseTime.split("-")[0] +"-" +browseTime.split("-")[1]+"-"+year;
        System.out.println(browseTime);
    }

}
