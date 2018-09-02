package net.perceptio.heatstore.api.model;

import com.fasterxml.jackson.annotation.JsonIgnore;

import javax.persistence.*;
import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

@Entity
public class Role {
    @Id
    private String id;
    private String description;
    @ManyToMany(fetch = FetchType.EAGER, cascade = CascadeType.ALL)
    @JoinTable(name = "ROLE_ACTIONS", joinColumns = {
            @JoinColumn(name = "ROLE_ID", nullable = false, updatable = false)},
            inverseJoinColumns = {@JoinColumn(name = "ACTION_ID",
                    nullable = false, updatable = false)})
    private Set<Action> actions = new HashSet<Action>(0);

    @ManyToMany(fetch = FetchType.LAZY, mappedBy = "roles")
    @JsonIgnore
    private Set<Camera> cameras = new HashSet<>(0);

    public Role() {
    }

    public Role(String id) {
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

    public Set<Action> getActions() {
        return actions;
    }

    public void setActions(Set<Action> actions) {
        this.actions = actions;
    }

    public Set<Camera> getCameras() {
        return cameras;
    }

    public void setCameras(Set<Camera> cameras) {
        this.cameras = cameras;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Role)) return false;
        Role role = (Role) o;
        return Objects.equals(getId(), role.getId()) &&
                Objects.equals(description, role.description);
    }

    @Override
    public int hashCode() {

        return Objects.hash(getId(), description);
    }

    @Override
    public String toString() {
        return "Role{" +
                "id='" + id + '\'' +
                ", description='" + description + '\'' +
                '}';
    }
}
