/* Small read-only Vulkan capability probe. Build with a platform Vulkan library. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <vulkan/vulkan.h>

static void fail(const char *operation, VkResult result) {
    fprintf(stderr, "%s failed: VkResult %d\n", operation, (int)result);
    exit(1);
}

static void print_json_string(const char *value) {
    putchar('"');
    for (const unsigned char *p = (const unsigned char *)value; *p; ++p) {
        if (*p == '"' || *p == '\\') {
            putchar('\\');
            putchar(*p);
        } else if (*p < 0x20) {
            printf("\\u%04x", *p);
        } else {
            putchar(*p);
        }
    }
    putchar('"');
}

static void print_format(VkPhysicalDevice device, VkFormat format, const char *name, int comma) {
    VkFormatProperties props;
    vkGetPhysicalDeviceFormatProperties(device, format, &props);
    printf("    \"%s\": {\"sampled\": %s, \"color_attachment\": %s, \"depth_attachment\": %s}%s\n",
           name,
           (props.optimalTilingFeatures & VK_FORMAT_FEATURE_SAMPLED_IMAGE_BIT) ? "true" : "false",
           (props.optimalTilingFeatures & VK_FORMAT_FEATURE_COLOR_ATTACHMENT_BIT) ? "true" : "false",
           (props.optimalTilingFeatures & VK_FORMAT_FEATURE_DEPTH_STENCIL_ATTACHMENT_BIT) ? "true" : "false",
           comma ? "," : "");
}

int main(void) {
    VkApplicationInfo app = {0};
    app.sType = VK_STRUCTURE_TYPE_APPLICATION_INFO;
    app.pApplicationName = "ps4-unreal-openorbis-capability-probe";
    app.apiVersion = VK_API_VERSION_1_0;

    VkInstanceCreateInfo create = {0};
    create.sType = VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO;
    create.pApplicationInfo = &app;
    VkInstance instance = VK_NULL_HANDLE;
    VkResult result = vkCreateInstance(&create, NULL, &instance);
    if (result != VK_SUCCESS) fail("vkCreateInstance", result);

    uint32_t count = 0;
    result = vkEnumeratePhysicalDevices(instance, &count, NULL);
    if (result != VK_SUCCESS) fail("vkEnumeratePhysicalDevices count", result);
    VkPhysicalDevice *devices = count ? calloc(count, sizeof(*devices)) : NULL;
    if (count && !devices) { fprintf(stderr, "Out of memory\n"); return 1; }
    if (count) {
        result = vkEnumeratePhysicalDevices(instance, &count, devices);
        if (result != VK_SUCCESS) fail("vkEnumeratePhysicalDevices", result);
    }
    printf("{\n  \"device_count\": %u,\n  \"devices\": [\n", count);
    for (uint32_t i = 0; i < count; ++i) {
        VkPhysicalDeviceProperties props;
        VkPhysicalDeviceFeatures features;
        VkPhysicalDeviceMemoryProperties memory;
        vkGetPhysicalDeviceProperties(devices[i], &props);
        vkGetPhysicalDeviceFeatures(devices[i], &features);
        vkGetPhysicalDeviceMemoryProperties(devices[i], &memory);

        uint32_t extension_count = 0;
        result = vkEnumerateDeviceExtensionProperties(devices[i], NULL, &extension_count, NULL);
        if (result != VK_SUCCESS) fail("extension count", result);
        VkExtensionProperties *extensions = extension_count ? calloc(extension_count, sizeof(*extensions)) : NULL;
        if (extension_count && !extensions) { fprintf(stderr, "Out of memory\n"); return 1; }
        if (extension_count) {
            result = vkEnumerateDeviceExtensionProperties(devices[i], NULL, &extension_count, extensions);
            if (result != VK_SUCCESS && result != VK_INCOMPLETE) fail("device extensions", result);
        }
        printf("    {\n      \"name\": ");
        print_json_string(props.deviceName);
        printf(",\n");
        printf("      \"api_version\": \"%u.%u.%u\",\n",
               VK_VERSION_MAJOR(props.apiVersion), VK_VERSION_MINOR(props.apiVersion),
               VK_VERSION_PATCH(props.apiVersion));
        printf("      \"vendor_id\": %u, \"device_id\": %u,\n", props.vendorID, props.deviceID);
        printf("      \"limits\": {\"max_image_2d\": %u, \"max_color_attachments\": %u, \"max_uniform_buffer_range\": %u},\n",
               props.limits.maxImageDimension2D, props.limits.maxColorAttachments,
               props.limits.maxUniformBufferRange);
        printf("      \"features\": {\"sampler_anisotropy\": %s, \"geometry_shader\": %s, \"tessellation_shader\": %s, \"shader_int64\": %s, \"texture_compression_bc\": %s},\n",
               features.samplerAnisotropy ? "true" : "false",
               features.geometryShader ? "true" : "false",
               features.tessellationShader ? "true" : "false",
               features.shaderInt64 ? "true" : "false",
               features.textureCompressionBC ? "true" : "false");
        printf("      \"memory_heaps\": [");
        for (uint32_t j = 0; j < memory.memoryHeapCount; ++j) {
            printf("%s%llu", j ? ", " : "", (unsigned long long)memory.memoryHeaps[j].size);
        }
        printf("],\n      \"extensions\": [");
        for (uint32_t j = 0; j < extension_count; ++j) {
            printf("%s", j ? ", " : "");
            print_json_string(extensions[j].extensionName);
        }
        printf("],\n      \"optimal_tiling_formats\": {\n");
        print_format(devices[i], VK_FORMAT_R8G8B8A8_UNORM, "rgba8", 1);
        print_format(devices[i], VK_FORMAT_R16G16B16A16_SFLOAT, "rgba16f", 1);
        print_format(devices[i], VK_FORMAT_BC7_UNORM_BLOCK, "bc7", 1);
        print_format(devices[i], VK_FORMAT_D32_SFLOAT, "d32", 0);
        printf("      }\n    }%s\n", i + 1 < count ? "," : "");
        free(extensions);
    }
    printf("  ]\n}\n");
    free(devices);
    vkDestroyInstance(instance, NULL);
    return 0;
}
