# Rank Math SEO API Extension

## Description

This WordPress extension adds Rank Math SEO metadata (meta title and meta description) to the WordPress REST API.

By default, WordPress does not expose the custom fields used by Rank Math SEO (`rank_math_title` and `rank_math_description`) in its REST API. This plugin solves this problem by allowing these data to be optionally included.

## Prerequisites

- WordPress 5.0+
- [Rank Math SEO](https://wordpress.org/plugins/seo-by-rank-math/) plugin installed and configured

## Installation

1. Download the `rank-math-seo-api-extension` folder
2. Upload it to the `/wp-content/plugins/` directory of your WordPress site
3. Activate the plugin from the "Plugins" menu in the WordPress admin

## Configuration

1. Go to "Settings > Rank Math SEO API" in the WordPress admin
2. Check the "Enable Rank Math SEO in REST API" box
3. Click "Save Changes"

## Usage

Once activated, the extension will automatically add the `rank_math_title` and `rank_math_description` fields to the REST API responses for posts and pages.

### Request Example

```
GET /wp-json/wp/v2/posts/{POST_ID}
```

### Response Example (with the extension activated)

```json
{
  "id": 123,
  "title": {
    "rendered": "Post Title"
  },
  "content": {
    "rendered": "<p>Post content...</p>"
  },
  "rank_math_title": "SEO optimized title for this post | Site Name",
  "rank_math_description": "Here is an SEO optimized meta description that accurately describes the content of this post."
}
```

## Testing and Verification

To verify that the extension is working correctly:

1. Make sure the data is properly filled in Rank Math (check the "Edit Snippet" tab in the post editor)
2. Access `https://your-site.com/wp-json/wp/v2/posts/123` (replace 123 with a post ID)
3. Verify that the `rank_math_title` and `rank_math_description` fields are present in the JSON response

You can also test with and without the option enabled to confirm that the fields only appear when the option is activated.

## Troubleshooting

### Rank Math fields do not appear in the REST API

1. Check that the option is enabled in "Settings > Rank Math SEO API"
2. Make sure Rank Math SEO is properly installed and the fields are filled in
3. Check that no security plugin or firewall is blocking the WordPress REST API

### Access Permissions

By default, metadata is only visible to users with editing rights (`edit_posts`). If you need to modify this restriction, you can adjust the `permission_callback` in the `register_rank_math_meta()` function.

## Custom Content Type Support

The extension supports posts (`post`) and pages (`page`) by default. If you need to add support for other custom content types, you can add additional filters in your `functions.php` file:

```php
// Example for a custom content type 'product'
add_filter('rest_prepare_product', 'expose_rank_math_meta_to_rest', 10, 3);
