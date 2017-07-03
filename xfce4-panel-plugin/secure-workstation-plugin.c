#include <libxfce4panel/xfce-panel-plugin.h>
#include <string.h>

static void constructor(XfcePanelPlugin *plugin);
XFCE_PANEL_PLUGIN_REGISTER_INTERNAL(constructor);

static void
print_hello (GtkWidget *widget,
             gpointer   data)
{
  g_print ("Hello World\n");
}

static void
constructor(XfcePanelPlugin *plugin) { 
    GtkWidget *window = gtk_socket_new();
    GtkWidget *button;
    GtkWidget *button_box;

    //window = gtk_application_window_new (NULL, NULL);
    //gtk_window_set_title (GTK_WINDOW (window), "Window");
    //gtk_window_set_default_size (GTK_WINDOW (window), 200, 200);


    //GtkWidget *ebox = gtk_event_box_new();

    //button_box = gtk_button_box_new (GTK_ORIENTATION_HORIZONTAL);
    //gtk_container_add (GTK_CONTAINER (ebox), button_box);

    // button = gtk_button_new_with_label ("Hello World");
    // g_signal_connect (button, "clicked", G_CALLBACK (print_hello), NULL);
    // gtk_container_add (GTK_CONTAINER (ebox), button);

    gtk_container_add(GTK_CONTAINER(plugin), window);
    gtk_widget_show_all(window);
    xfce_panel_plugin_set_expand (XFCE_PANEL_PLUGIN(plugin), TRUE);
}
