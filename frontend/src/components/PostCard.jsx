import { Box, Text, Heading, Button, HStack, VStack, Input } from "@chakra-ui/react";
import API from "../api";
import { useState, useEffect } from "react";
import { getUserFromToken } from "../auth";

export default function PostCard({ post, refresh }) {
  const [commentText, setCommentText] = useState("");
  const [comments, setComments] = useState([]);
  const user = getUserFromToken();

  const loadComments = async () => {
    const res = await API.get(`/posts/${post._id}/comments`);
    setComments(res.data);
  };

  useEffect(() => {
    loadComments();
  }, [post._id]);

  const like = async () => {
    if (!user) {
      alert("Login required to like");
      return;
    }
    await API.post(`/posts/${post._id}/like`, {}, {
      headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
    });
    refresh();
  };

  const addComment = async () => {
    if (!user) {
      alert("Login required to comment");
      return;
    }
    if (!commentText.trim()) return;

    await API.post(
      `/posts/${post._id}/comment`,
      {
        username: user.username,
        text: commentText,
      },
      {
        headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
      }
    );
    setCommentText("");
    await loadComments(); 
  };

  return (
    <Box borderWidth="1px" borderRadius="md" p={4} my={3}>
      <Heading size="sm">{post.title}</Heading>
      <Text>{post.content}</Text>
      <Text fontSize="sm" color="gray.500">By {post.username || "unknown"}</Text>
      <HStack mt={3}>
        <Button size="sm" onClick={like}>Like ({post.likes || 0})</Button>
      </HStack>
      <VStack mt={4} align="stretch" spacing={2}>
        <Heading size="xs" color="gray.600">Comments ({comments.length})</Heading>
        {comments.map((c) => (
          <Box key={c._id} p={2} bg="gray.50" borderRadius="md">
            <Text fontWeight="bold" fontSize="sm">
              {c.username}
            </Text>
            <Text fontSize="sm">{c.text}</Text>
          </Box>
        ))}
        <HStack mt={2}><Input value={commentText} placeholder="Add a comment..." onChange={(e) => setCommentText(e.target.value)}/>
          <Button size="sm" onClick={addComment}>Comment</Button>
        </HStack>
      </VStack>
    </Box>
  );
}
