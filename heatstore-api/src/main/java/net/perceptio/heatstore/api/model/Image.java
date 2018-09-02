package net.perceptio.heatstore.api.model;

import com.fasterxml.jackson.annotation.JsonIgnore;

import javax.persistence.*;
import java.sql.Timestamp;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;


@Entity
public class Image {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private Timestamp date;
    @ManyToMany(mappedBy = "images")
    @JsonIgnore
    List<Person> persons = new ArrayList<>(0);
    @OneToMany(
            mappedBy = "image",
            cascade = CascadeType.ALL,
            orphanRemoval = true,
            fetch = FetchType.EAGER
    )
    private List<Detection> detections = new ArrayList<>(0);
    @ManyToOne
    private Camera camera;

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
        this.detections = detections.stream().map(detection -> {
            detection.setImage(this);
            return detection;
        }).collect(Collectors.toList());
    }


    public Camera getCamera() {
        return camera;
    }

    public void setCamera(Camera camera) {
        if (this.camera != null) {
            this.camera.removeImage(this);
        }
        camera.addImage(this);
        this.camera = camera;
    }

    public List<Person> getPersons() {
        return persons;
    }

    public void setPersons(List<Person> person) {
        this.persons = person;
    }

    public void addPerson(Person person) {
        getPersons().add(person);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Image)) return false;
        Image image = (Image) o;
        return Objects.equals(getId(), image.getId());
    }

    @Override
    public int hashCode() {

        return Objects.hash(getId());
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
