package net.perceptio.heatstore.api.config;

import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.cloud.config.java.AbstractCloudConfig;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.jdbc.datasource.lookup.JndiDataSourceLookup;

import javax.naming.NamingException;
import javax.sql.DataSource;


@Configuration
@EntityScan({"net.perceptio.heatstore.api.model"})
@EnableJpaRepositories({"net.perceptio.heatstore.api.controller.repository"})
@SuppressWarnings("unused")
public class CloudConfiguration extends AbstractCloudConfig {
    @Bean(destroyMethod = "")
    public DataSource jndiDataSource() throws IllegalArgumentException, NamingException {
        JndiDataSourceLookup dataSourceLookup = new JndiDataSourceLookup();

        DataSource ds = dataSourceLookup.getDataSource("java:comp/env/jdbc/DefaultDB");

        return ds;
    }
}
