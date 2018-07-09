package net.perceptio.heatstore.api.model;

import javax.persistence.*;
import java.sql.Timestamp;
import java.util.List;
import java.util.Objects;


@Entity
public class Image {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private Timestamp date;
    @OneToMany(
            mappedBy = "image",
            cascade = CascadeType.ALL,
            orphanRemoval = true,
            fetch = FetchType.EAGER
    )
    private List<Detection> detections;

    public Image() {
    }

    public Image(Long id) {
        this();
        this.id = id;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Timestamp getDate() {
        return date;
    }

    public void setDate(Timestamp date) {
        this.date = date;
    }

    public List<Detection> getDetections() {
        return detections;
    }

    public void setDetections(List<Detection> detections) {
        this.detections = detections;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Image)) return false;
        Image image = (Image) o;
        return Objects.equals(getId(), image.getId()) &&
                Objects.equals(getDate(), image.getDate()) &&
                Objects.equals(getDetections(), image.getDetections());
    }

    @Override
    public int hashCode() {
        return Objects.hash(getId(), getDate(), getDetections());
    }

    @Override
    public String toString() {
        return "Image{" +
                "id=" + id +
                ", date=" + date +
                ", detections=" + detections +
                '}';
    }
}
