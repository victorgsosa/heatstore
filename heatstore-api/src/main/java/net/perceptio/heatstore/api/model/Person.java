package net.perceptio.heatstore.api.model;

import org.hibernate.annotations.LazyCollection;
import org.hibernate.annotations.LazyCollectionOption;

import javax.persistence.*;
import java.io.Serializable;
import java.sql.Timestamp;
import java.util.*;

@Entity
public class Person implements Serializable {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Timestamp firstSeenOn;
    private Timestamp lastSeenOn;

    @ManyToMany(cascade = {CascadeType.ALL})
    @JoinTable(name = "PERSON_IN_IMAGE", joinColumns = {
            @JoinColumn(name = "PERSON_ID", nullable = false, updatable = false)},
            inverseJoinColumns = {@JoinColumn(name = "IMAGE_ID",
                    nullable = false, updatable = false)})
    @LazyCollection(LazyCollectionOption.EXTRA)
    private Set<Image> images = new HashSet<>(0);

    @OneToMany(
            mappedBy = "person",
            cascade = CascadeType.ALL,
            orphanRemoval = true
    )
    @LazyCollection(LazyCollectionOption.FALSE)
    private List<Embeddings> embeddings = new ArrayList<>(0);

    @OneToMany(
            mappedBy = "person",
            cascade = CascadeType.ALL,
            orphanRemoval = true
    )
    @LazyCollection(LazyCollectionOption.FALSE)
    private List<Classifier> classifiers = new ArrayList<>(0);

    public Person() {
    }

    public Person(Long id, Timestamp firstSeenOn, Timestamp lastSeenOn) {
        this.id = id;
        this.firstSeenOn = firstSeenOn;
        this.lastSeenOn = lastSeenOn;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Timestamp getFirstSeenOn() {
        return firstSeenOn;
    }

    public void setFirstSeenOn(Timestamp firstSeenOn) {
        this.firstSeenOn = firstSeenOn;
    }

    public Timestamp getLastSeenOn() {
        return lastSeenOn;
    }

    public void setLastSeenOn(Timestamp lastSeenOn) {
        this.lastSeenOn = lastSeenOn;
    }

    public Set<Image> getImages() {
        return images;
    }

    public void setImages(Set<Image> images) {
        this.images = images;
        images.stream().forEach(i -> i.addPerson(this));
    }

    public void addImage(Image image) {
        getImages().add(image);
        image.addPerson(this);
    }

    public void addImages(Collection<Image> images) {
        getImages().addAll(images);
        images.stream().forEach(i -> i.addPerson(this));
    }

    public List<Embeddings> getEmbeddings() {
        return embeddings;
    }

    public void setEmbeddings(List<Embeddings> embeddings) {
        this.embeddings = embeddings;
        embeddings.stream().forEach(e -> e.setPerson(this));
    }

    public List<Classifier> getClassifiers() {
        return classifiers;
    }

    public void setClassifiers(List<Classifier> classifiers) {
        this.classifiers = classifiers;
        classifiers.stream().forEach(c -> c.setPerson(this));
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Person)) return false;
        Person person = (Person) o;
        return Objects.equals(getId(), person.getId()) &&
                Objects.equals(getFirstSeenOn(), person.getFirstSeenOn()) &&
                Objects.equals(getLastSeenOn(), person.getLastSeenOn()) &&
                Objects.equals(getEmbeddings(), person.getEmbeddings()) &&
                Objects.equals(getClassifiers(), person.getClassifiers());
    }

    @Override
    public int hashCode() {

        return Objects.hash(getId(), getFirstSeenOn(), getLastSeenOn(), getEmbeddings(), getClassifiers());
    }

    @Override
    public String toString() {
        return "Person{" +
                "id=" + id +
                ", firstSeenOn=" + firstSeenOn +
                ", lastSeenOn=" + lastSeenOn +
                ", embeddings=" + embeddings +
                ", classifiers=" + classifiers +
                '}';
    }
}
