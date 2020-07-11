package com.df.bbt.entity;

import java.io.Serializable;

/**
 * (Browse)实体类
 *
 * @author makejava
 * @since 2020-04-26 15:54:28
 */
public class Browse implements Serializable {
    private static final long serialVersionUID = -54719269182169437L;
    
    private String browseTime;
    
    private Integer userId;
    
    private Integer goodsId;
    
    private Double browsePrice;


    public String getBrowseTime() {
        return browseTime;
    }

    public void setBrowseTime(String browseTime) {
        this.browseTime = browseTime;
    }

    public Integer getUserId() {
        return userId;
    }

    public void setUserId(Integer userId) {
        this.userId = userId;
    }

    public Integer getGoodsId() {
        return goodsId;
    }

    public void setGoodsId(Integer goodsId) {
        this.goodsId = goodsId;
    }

    public Double getBrowsePrice() {
        return browsePrice;
    }

    public void setBrowsePrice(Double browsePrice) {
        this.browsePrice = browsePrice;
    }

}