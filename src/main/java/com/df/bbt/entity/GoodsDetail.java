package com.df.bbt.entity;

import java.io.Serializable;

/**
 * (GoodsDetail)实体类
 *
 * @author makejava
 * @since 2020-04-26 15:46:53
 */
public class GoodsDetail implements Serializable {
    private static final long serialVersionUID = 718385669673876642L;
    
    private Integer goodsId;
    
    private String goodsEva;
    
    private String goodsTitle;
    
    private Integer gmId;
    
    private String goodsUrl;
    
    private String source;
    
    private String goodsPrice;
    
    private String goodsDegree;
    
    private String searchImg;
    
    private String smallImg1;
    
    private String bigImg1;
    
    private String smallImg2;
    
    private String bigImg2;
    
    private String smallImg3;
    
    private String bigImg3;
    
    private String shop;
    
    private String screenSize;
    
    private String batteryCap;
    
    private String cpu;
    
    private String phoneMemory;
    
    private String runningMemory;
    
    private String model;
    
    private String graphicsCard;
    
    private String batteryLife;
    
    private String brand;


    public Integer getGoodsId() {
        return goodsId;
    }

    public void setGoodsId(Integer goodsId) {
        this.goodsId = goodsId;
    }

    public String getGoodsEva() {
        return goodsEva;
    }

    public void setGoodsEva(String goodsEva) {
        this.goodsEva = goodsEva;
    }

    public String getGoodsTitle() {
        return goodsTitle;
    }

    public void setGoodsTitle(String goodsTitle) {
        this.goodsTitle = goodsTitle;
    }

    public Integer getGmId() {
        return gmId;
    }

    public void setGmId(Integer gmId) {
        this.gmId = gmId;
    }

    public String getGoodsUrl() {
        return goodsUrl;
    }

    public void setGoodsUrl(String goodsUrl) {
        this.goodsUrl = goodsUrl;
    }

    public String getSource() {
        return source;
    }

    public void setSource(String source) {
        this.source = source;
    }

    public String getGoodsPrice() {
        return goodsPrice;
    }

    public void setGoodsPrice(String goodsPrice) {
        this.goodsPrice = goodsPrice;
    }

    public String getGoodsDegree() {
        return goodsDegree;
    }

    public void setGoodsDegree(String goodsDegree) {
        this.goodsDegree = goodsDegree;
    }

    public String getSearchImg() {
        return searchImg;
    }

    public void setSearchImg(String searchImg) {
        this.searchImg = searchImg;
    }

    public String getSmallImg1() {
        return smallImg1;
    }

    public void setSmallImg1(String smallImg1) {
        this.smallImg1 = smallImg1;
    }

    public String getBigImg1() {
        return bigImg1;
    }

    public void setBigImg1(String bigImg1) {
        this.bigImg1 = bigImg1;
    }

    public String getSmallImg2() {
        return smallImg2;
    }

    public void setSmallImg2(String smallImg2) {
        this.smallImg2 = smallImg2;
    }

    public String getBigImg2() {
        return bigImg2;
    }

    public void setBigImg2(String bigImg2) {
        this.bigImg2 = bigImg2;
    }

    public String getSmallImg3() {
        return smallImg3;
    }

    public void setSmallImg3(String smallImg3) {
        this.smallImg3 = smallImg3;
    }

    public String getBigImg3() {
        return bigImg3;
    }

    public void setBigImg3(String bigImg3) {
        this.bigImg3 = bigImg3;
    }

    public String getShop() {
        return shop;
    }

    public void setShop(String shop) {
        this.shop = shop;
    }

    public String getScreenSize() {
        return screenSize;
    }

    public void setScreenSize(String screenSize) {
        this.screenSize = screenSize;
    }

    public String getBatteryCap() {
        return batteryCap;
    }

    public void setBatteryCap(String batteryCap) {
        this.batteryCap = batteryCap;
    }

    public String getCpu() {
        return cpu;
    }

    public void setCpu(String cpu) {
        this.cpu = cpu;
    }

    public String getPhoneMemory() {
        return phoneMemory;
    }

    public void setPhoneMemory(String phoneMemory) {
        this.phoneMemory = phoneMemory;
    }

    public String getRunningMemory() {
        return runningMemory;
    }

    public void setRunningMemory(String runningMemory) {
        this.runningMemory = runningMemory;
    }

    public String getModel() {
        return model;
    }

    public void setModel(String model) {
        this.model = model;
    }

    public String getGraphicsCard() {
        return graphicsCard;
    }

    public void setGraphicsCard(String graphicsCard) {
        this.graphicsCard = graphicsCard;
    }

    public String getBatteryLife() {
        return batteryLife;
    }

    public void setBatteryLife(String batteryLife) {
        this.batteryLife = batteryLife;
    }

    public String getBrand() {
        return brand;
    }

    public void setBrand(String brand) {
        this.brand = brand;
    }

    @Override
    public String toString() {
        return "GoodsDetail{" +
                "goodsId=" + goodsId +
                ", goodsEva='" + goodsEva + '\'' +
                ", goodsTitle='" + goodsTitle + '\'' +
                ", gmId=" + gmId +
                ", goodsUrl='" + goodsUrl + '\'' +
                ", source='" + source + '\'' +
                ", goodsPrice='" + goodsPrice + '\'' +
                ", goodsDegree='" + goodsDegree + '\'' +
                ", searchImg='" + searchImg + '\'' +
                ", smallImg1='" + smallImg1 + '\'' +
                ", bigImg1='" + bigImg1 + '\'' +
                ", smallImg2='" + smallImg2 + '\'' +
                ", bigImg2='" + bigImg2 + '\'' +
                ", smallImg3='" + smallImg3 + '\'' +
                ", bigImg3='" + bigImg3 + '\'' +
                ", shop='" + shop + '\'' +
                ", screenSize='" + screenSize + '\'' +
                ", batteryCap='" + batteryCap + '\'' +
                ", cpu='" + cpu + '\'' +
                ", phoneMemory='" + phoneMemory + '\'' +
                ", runningMemory='" + runningMemory + '\'' +
                ", model='" + model + '\'' +
                ", graphicsCard='" + graphicsCard + '\'' +
                ", batteryLife='" + batteryLife + '\'' +
                ", brand='" + brand + '\'' +
                '}';
    }

    public String get(String name) {
        switch (name) {
            case "GOODS_TITLE":
                return goodsTitle;
            case "SEARCH_IMG":
                return searchImg;
            case "GOODS_PRICE":
                return goodsPrice;
            case "screen_size":
                return screenSize;
            case "battery_cap":
                return batteryCap;
            case "cpu":
                return cpu;
            case "phone_memory":
                return phoneMemory;
            case "running_memory":
                return runningMemory;
            case "model":
                return model;
            case "graphics_card":
                return graphicsCard;
            case "battery_life":
                return batteryLife;
            case "brand":
                return brand;
            default:
                return "";
        }
    }
}