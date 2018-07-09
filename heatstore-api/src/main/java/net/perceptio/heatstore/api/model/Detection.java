package net.perceptio.heatstore.api.model;


import com.fasterxml.jackson.annotation.JsonIgnore;

import javax.persistence.*;
import java.util.Objects;

@Entity
public class Detection {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    @ManyToOne
    @JsonIgnore
    private Image image;
    private Double score;
    private Double xMin;
    private Double yMin;
    private Double xMax;
    private Double yMax;
    private Double x;
    private Double y;

    public Detection() {
    }

    public Detection(Long id) {
        this.id = id;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Image getImage() {
        return image;
    }

    public void setImage(Image image) {
        this.image = image;
    }

    public Double getScore() {
        return score;
    }

    public void setScore(Double score) {
        this.score = score;
    }

    public Double getxMin() {
        return xMin;
    }

    public void setxMin(Double xMin) {
        this.xMin = xMin;
    }

    public Double getyMin() {
        return yMin;
    }

    public void setyMin(Double yMin) {
        this.yMin = yMin;
    }

    public Double getxMax() {
        return xMax;
    }

    public void setxMax(Double xMax) {
        this.xMax = xMax;
    }

    public Double getyMax() {
        return yMax;
    }

    public void setyMax(Double yMax) {
        this.yMax = yMax;
    }

    public Double getX() {
        return x;
    }

    public void setX(Double x) {
        this.x = x;
    }

    public Double getY() {
        return y;
    }

    public void setY(Double y) {
        this.y = y;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Detection)) return false;
        Detection detection = (Detection) o;
        return Objects.equals(getId(), detection.getId()) &&
                Objects.equals(getImage().getId(), detection.getImage().getId()) &&
                Objects.equals(getScore(), detection.getScore()) &&
                Objects.equals(getxMin(), detection.getxMin()) &&
                Objects.equals(getyMin(), detection.getyMin()) &&
                Objects.equals(getxMax(), detection.getxMax()) &&
                Objects.equals(getyMax(), detection.getyMax()) &&
                Objects.equals(getX(), detection.getX()) &&
                Objects.equals(getY(), detection.getY());
    }

    @Override
    public int hashCode() {

        return Objects.hash(getId(), getImage().getId(), getScore(), getxMin(), getyMin(), getxMax(), getyMax(), getX(), getY());
    }

    @Override
    public String toString() {
        return "Detection{" +
                "id=" + id +
                ", image=" + image.getId() +
                ", score=" + score +
                ", xMin=" + xMin +
                ", yMin=" + yMin +
                ", xMax=" + xMax +
                ", yMax=" + yMax +
                ", x=" + x +
                ", y=" + y +
                '}';
    }
}
