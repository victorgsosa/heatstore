package net.perceptio.heatstore.api.model;

import com.fasterxml.jackson.annotation.JsonIgnore;

import javax.persistence.*;
import java.util.*;

@Entity
public class Camera {
    @Id
    private String id;
    private Double height;
    private Double focalLength;

    private Double aDistance;
    private Double aX;
    private Double aY;

    private Double bDistance;
    private Double bX;
    private Double bY;

    private Double cDistance;
    private Double cX;
    private Double cY;

    @ManyToMany(fetch = FetchType.EAGER, cascade = CascadeType.ALL)
    @JoinTable(name = "CAMERA_ROLES", joinColumns = {
            @JoinColumn(name = "CAMERA_ID", nullable = false, updatable = false)},
            inverseJoinColumns = {@JoinColumn(name = "ROLE_ID",
                    nullable = false, updatable = false)})
    private Set<Role> roles = new HashSet<>(0);

    @OneToMany(
            mappedBy = "camera",
            cascade = CascadeType.ALL,
            orphanRemoval = true,
            fetch = FetchType.EAGER
    )
    @JsonIgnore
    private List<Image> images = new ArrayList<>();

    public Camera() {
    }

    public Camera(String id) {
        this.id = id;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public Double getHeight() {
        return height;
    }

    public void setHeight(Double height) {
        this.height = height;
    }

    public Double getFocalLength() {
        return focalLength;
    }

    public void setFocalLength(Double focalLength) {
        this.focalLength = focalLength;
    }

    public Double getaDistance() {
        return aDistance;
    }

    public void setaDistance(Double aDistance) {
        this.aDistance = aDistance;
    }

    public Double getaX() {
        return aX;
    }

    public void setaX(Double aX) {
        this.aX = aX;
    }

    public Double getaY() {
        return aY;
    }

    public void setaY(Double aY) {
        this.aY = aY;
    }

    public Double getbDistance() {
        return bDistance;
    }

    public void setbDistance(Double bDistance) {
        this.bDistance = bDistance;
    }

    public Double getbX() {
        return bX;
    }

    public void setbX(Double bX) {
        this.bX = bX;
    }

    public Double getbY() {
        return bY;
    }

    public void setbY(Double bY) {
        this.bY = bY;
    }

    public Double getcDistance() {
        return cDistance;
    }

    public void setcDistance(Double cDistance) {
        this.cDistance = cDistance;
    }

    public Double getcX() {
        return cX;
    }

    public void setcX(Double cX) {
        this.cX = cX;
    }

    public Double getcY() {
        return cY;
    }

    public void setcY(Double cY) {
        this.cY = cY;
    }

    public Set<Role> getRoles() {
        return roles;
    }

    public void setRoles(Set<Role> roles) {
        this.roles = roles;
    }

    public List<Image> getImages() {
        return images;
    }

    public void setImages(List<Image> images) {
        this.images = images;
    }

    public void addImage(Image image) {
        getImages().add(image);
    }

    public void removeImage(Image image) {
        getImages().remove(image);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Camera)) return false;
        Camera camera = (Camera) o;
        return Objects.equals(getId(), camera.getId()) &&
                Objects.equals(getHeight(), camera.getHeight()) &&
                Objects.equals(getFocalLength(), camera.getFocalLength()) &&
                Objects.equals(getaDistance(), camera.getaDistance()) &&
                Objects.equals(getaX(), camera.getaX()) &&
                Objects.equals(getaY(), camera.getaY()) &&
                Objects.equals(getbDistance(), camera.getbDistance()) &&
                Objects.equals(getbX(), camera.getbX()) &&
                Objects.equals(getbY(), camera.getbY()) &&
                Objects.equals(getcDistance(), camera.getcDistance()) &&
                Objects.equals(getcX(), camera.getcX()) &&
                Objects.equals(getcY(), camera.getcY()) &&
                Objects.equals(getRoles(), camera.getRoles());
    }

    @Override
    public int hashCode() {

        return Objects.hash(getId(), getHeight(), getFocalLength(), getaDistance(), getaX(), getaY(), getbDistance(), getbX(), getbY(), getcDistance(), getcX(), getcY(), getRoles());
    }

    @Override
    public String toString() {
        return "Camera{" +
                "id='" + id + '\'' +
                ", height=" + height +
                ", focalLength=" + focalLength +
                ", aDistance=" + aDistance +
                ", aX=" + aX +
                ", aY=" + aY +
                ", bDistance=" + bDistance +
                ", bX=" + bX +
                ", bY=" + bY +
                ", cDistance=" + cDistance +
                ", cX=" + cX +
                ", cY=" + cY +
                ", roles=" + roles +
                '}';
    }
}
