package ut.io.tintoy.confluence.plugin.docfx_import;

import org.junit.Test;
import io.tintoy.confluence.plugin.docfx_import.api.PluginComponent;
import io.tintoy.confluence.plugin.docfx_import.impl.PluginComponentImpl;

import static org.junit.Assert.assertEquals;

public class PluginComponentUnitTest
{
    @Test
    public void testMyName()
    {
        PluginComponent component = new PluginComponentImpl(null);
        assertEquals("names do not match!", "pluginComponent",component.getName());
    }
}