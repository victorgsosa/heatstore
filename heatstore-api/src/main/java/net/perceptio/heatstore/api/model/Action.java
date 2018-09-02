package net.perceptio.heatstore.api.model;

import com.fasterxml.jackson.annotation.JsonIgnore;

import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.Id;
import javax.persistence.ManyToMany;
import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

@Entity
public class Action {
    @Id
    private String id;
    private String description;
    @ManyToMany(fetch = FetchType.LAZY, mappedBy = "actions")
    @JsonIgnore
    private Set<Role> roles = new HashSet<>(0);

    public Action() {
    }

    public Action(String id) {
        this.id = id;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public Set<Role> getRoles() {
        return roles;
    }

    public void setRoles(Set<Role> roles) {
        this.roles = roles;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Action)) return false;
        Action action = (Action) o;
        return Objects.equals(getId(), action.getId()) &&
                Objects.equals(description, action.description);
    }

    @Override
    public int hashCode() {

        return Objects.hash(getId(), description);
    }

    @Override
    public String toString() {
        return "Action{" +
                "id='" + id + '\'' +
                ", description='" + description + '\'' +
                '}';
    }
}
