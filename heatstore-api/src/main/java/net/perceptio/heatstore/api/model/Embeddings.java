package net.perceptio.heatstore.api.model;

import com.fasterxml.jackson.annotation.JsonIgnore;

import javax.persistence.*;
import java.io.Serializable;
import java.util.Objects;

@Entity
@Table(name = "PERSON_EMBEDDINGS")
@IdClass(Embeddings.EmbeddingsKey.class)
public class Embeddings {
    @MapsId
    @ManyToOne
    @JsonIgnore
    private Person person;
    @Id
    @Column(name = "SEQ")
    private Integer sequence;
    private Double value;

    public Embeddings() {
    }

    public Embeddings(Person person, Integer sequence, Double value) {
        this.person = person;
        this.sequence = sequence;
        this.value = value;
    }

    public Person getPerson() {
        return person;
    }

    public void setPerson(Person person) {
        this.person = person;
    }

    public Integer getSequence() {
        return sequence;
    }

    public void setSequence(Integer sequence) {
        this.sequence = sequence;
    }

    public Double getValue() {
        return value;
    }

    public void setValue(Double value) {
        this.value = value;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Embeddings)) return false;
        Embeddings that = (Embeddings) o;
        return Objects.equals(getSequence(), that.getSequence()) &&
                Objects.equals(getValue(), that.getValue());
    }

    @Override
    public int hashCode() {

        return Objects.hash(getSequence(), getValue());
    }

    @Override
    public String toString() {
        return "Embeddings{" +
                "sequence=" + sequence +
                ", value=" + value +
                '}';
    }

    public static class EmbeddingsKey implements Serializable {
        private Person person;
        private Integer sequence;

        public EmbeddingsKey() {
        }

        public EmbeddingsKey(Person person, Integer sequence) {
            this.person = person;
            this.sequence = sequence;
        }

        public Person getPerson() {
            return person;
        }

        public void setPerson(Person person) {
            this.person = person;
        }

        public Integer getSequence() {
            return sequence;
        }

        public void setSequence(Integer sequence) {
            this.sequence = sequence;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (!(o instanceof EmbeddingsKey)) return false;
            EmbeddingsKey that = (EmbeddingsKey) o;
            return Objects.equals(getSequence(), that.getSequence());
        }

        @Override
        public int hashCode() {

            return Objects.hash(getSequence());
        }

        @Override
        public String toString() {
            return "EmbeddingsKey{" +
                    "sequence=" + sequence +
                    '}';
        }
    }
}
