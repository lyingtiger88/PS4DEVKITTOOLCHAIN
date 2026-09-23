cmake_minimum_required(VERSION 3.15)
project(ps4_unreal_feasibility LANGUAGES C)

set(VULKAN_HEADERS_DIR "" CACHE PATH "Directory containing vulkan/vulkan.h")
find_path(VULKAN_INCLUDE_DIR vulkan/vulkan.h HINTS "${VULKAN_HEADERS_DIR}" REQUIRED)
find_library(VULKAN_LOADER NAMES vulkan libvulkan.so.1 REQUIRED)

add_executable(vulkan_capabilities probes/vulkan_capabilities.c)
target_compile_features(vulkan_capabilities PRIVATE c_std_11)
target_include_directories(vulkan_capabilities PRIVATE "${VULKAN_INCLUDE_DIR}")
target_link_libraries(vulkan_capabilities PRIVATE "${VULKAN_LOADER}")
if(CMAKE_C_COMPILER_ID MATCHES "GNU|Clang")
  target_compile_options(vulkan_capabilities PRIVATE -Wall -Wextra -Werror)
endif()
