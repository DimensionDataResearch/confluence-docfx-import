package it.io.tintoy.confluence.plugin.docfx_import;

import org.junit.Test;
import org.junit.runner.RunWith;
import com.atlassian.plugins.osgi.test.AtlassianPluginsTestRunner;
import io.tintoy.confluence.plugin.docfx_import.api.PluginComponent;
import com.atlassian.sal.api.ApplicationProperties;

import static org.junit.Assert.assertEquals;

@RunWith(AtlassianPluginsTestRunner.class)
public class PluginComponentWiredTest
{
    private final ApplicationProperties applicationProperties;
    private final PluginComponent pluginComponent;

    public PluginComponentWiredTest(ApplicationProperties applicationProperties,PluginComponent pluginComponent)
    {
        this.applicationProperties = applicationProperties;
        this.pluginComponent = pluginComponent;
    }

    @Test
    public void testMyName()
    {
        assertEquals("names do not match!", "pluginComponent:" + applicationProperties.getDisplayName(),pluginComponent.getName());
    }
}