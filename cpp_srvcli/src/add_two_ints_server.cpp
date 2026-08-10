#include <cinttypes>
#include <memory>

#include "tutorial_interfaces/srv/add_three_ints.hpp"
#include "rclcpp/rclcpp.hpp"

using AddThreeInts = tutorial_interfaces::srv::AddThreeInts;
rclcpp::Node::SharedPtr g_node = nullptr;

void handle_service(
  const std::shared_ptr<rmw_request_id_t> request_header,
  const std::shared_ptr<AddThreeInts::Request> request,
  const std::shared_ptr<AddThreeInts::Response> response)
{
  (void)request_header;
  RCLCPP_INFO(
    g_node->get_logger(),
    "request: %" PRId64 " + %" PRId64 " + %" PRId64, request->a, request->b, request->c);
  response->sum = request->a + request->b + request->c;
}

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  g_node = rclcpp::Node::make_shared("minimal_service");
  auto server = g_node->create_service<AddThreeInts>("add_three_ints", handle_service);
  rclcpp::spin(g_node);
  rclcpp::shutdown();
  g_node = nullptr;
  return 0;
}
