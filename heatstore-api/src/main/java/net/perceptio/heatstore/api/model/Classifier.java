package net.perceptio.heatstore.api.model;

import com.fasterxml.jackson.annotation.JsonIgnore;

import javax.persistence.*;
import java.io.Serializable;
import java.util.Objects;

@Entity
@Table(name = "PERSON_CLASSIFIER")
@IdClass(Classifier.ClassifierKey.class)
public class Classifier implements Serializable {
    @MapsId
    @ManyToOne
    @JsonIgnore
    private Person person;

    @Id
    private String name;

    private Double value;

    private Double probability;

    public Classifier() {
    }

    public Person getPerson() {
        return person;
    }

    public void setPerson(Person person) {
        this.person = person;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Double getValue() {
        return value;
    }

    public void setValue(Double value) {
        this.value = value;
    }

    public Double getProbability() {
        return probability;
    }

    public void setProbability(Double probability) {
        this.probability = probability;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Classifier)) return false;
        Classifier that = (Classifier) o;
        return Objects.equals(getName(), that.getName()) &&
                Objects.equals(getValue(), that.getValue()) &&
                Objects.equals(getProbability(), that.getProbability());
    }

    @Override
    public int hashCode() {

        return Objects.hash(getName(), getValue(), getProbability());
    }

    @Override
    public String toString() {
        return "Classifier{" +
                "name='" + name + '\'' +
                ", value=" + value +
                ", probability=" + probability +
                '}';
    }

    public static class ClassifierKey implements Serializable {
        private Person person;
        private String name;

        public ClassifierKey() {
        }

        public ClassifierKey(Person person, String name) {
            this.person = person;
            this.name = name;
        }

        public Person getPerson() {
            return person;
        }

        public void setPerson(Person person) {
            this.person = person;
        }

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (!(o instanceof ClassifierKey)) return false;
            ClassifierKey that = (ClassifierKey) o;
            return Objects.equals(getName(), that.getName());
        }

        @Override
        public int hashCode() {

            return Objects.hash(getName());
        }

        @Override
        public String toString() {
            return "ClassifierKey{" +
                    "name='" + name + '\'' +
                    '}';
        }
    }
}
