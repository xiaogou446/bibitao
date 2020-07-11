package com.df.bbt;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@MapperScan(value = "com.df.bbt.mapper")
@SpringBootApplication
public class BbtApplication {

    public static void main(String[] args) {
        SpringApplication.run(BbtApplication.class, args);
    }

}
