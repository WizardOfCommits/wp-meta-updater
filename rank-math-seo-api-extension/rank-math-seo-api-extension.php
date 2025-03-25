<?php
/**
 * Plugin Name: Rank Math SEO API Extension
 * Plugin URI: https://example.com/plugins/rank-math-seo-api-extension
 * Description: Ajoute les métadonnées Rank Math SEO (title et description) à l'API REST WordPress.
 * Version: 1.0.0
 * Author: William Troillard
 * Author URI: https://qontent.fr
 * Text Domain: rank-math-seo-api-extension
 * Domain Path: /languages
 */

// Empêcher l'accès direct au fichier
if (!defined('ABSPATH')) {
    exit; // Sortie si accès direct
}

/**
 * Enregistre les champs personnalisés de Rank Math pour l'API REST
 */
function register_rank_math_meta() {
    // Vérifier si l'option est activée
    $enable_rank_math_seo = get_option('enable_rank_math_seo_api', false);
    
    // Ne pas enregistrer les meta si l'option est désactivée
    if (!$enable_rank_math_seo) {
        return;
    }
    
    // Enregistrer rank_math_title pour les articles
    register_meta('post', 'rank_math_title', [
        'object_subtype' => 'post',
        'type' => 'string',
        'single' => true,
        'sanitize_callback' => 'sanitize_text_field',
        'show_in_rest' => [
            'schema' => [
                'type' => 'string',
                'description' => 'RankMath SEO Title',
                'context' => ['view', 'edit'],
            ],
            'permission_callback' => function() { return current_user_can('edit_posts'); },
        ],
    ]);

    // Enregistrer rank_math_title pour les pages
    register_meta('post', 'rank_math_title', [
        'object_subtype' => 'page',
        'type' => 'string',
        'single' => true,
        'sanitize_callback' => 'sanitize_text_field',
        'show_in_rest' => [
            'schema' => [
                'type' => 'string',
                'description' => 'RankMath SEO Title',
                'context' => ['view', 'edit'],
            ],
            'permission_callback' => function() { return current_user_can('edit_pages'); },
        ],
    ]);

    // Enregistrer rank_math_description pour les articles
    register_meta('post', 'rank_math_description', [
        'object_subtype' => 'post',
        'type' => 'string',
        'single' => true,
        'sanitize_callback' => 'sanitize_text_field',
        'show_in_rest' => [
            'schema' => [
                'type' => 'string',
                'description' => 'RankMath SEO Description',
                'context' => ['view', 'edit'],
            ],
            'permission_callback' => function() { return current_user_can('edit_posts'); },
        ],
    ]);

    // Enregistrer rank_math_description pour les pages
    register_meta('post', 'rank_math_description', [
        'object_subtype' => 'page',
        'type' => 'string',
        'single' => true,
        'sanitize_callback' => 'sanitize_text_field',
        'show_in_rest' => [
            'schema' => [
                'type' => 'string',
                'description' => 'RankMath SEO Description',
                'context' => ['view', 'edit'],
            ],
            'permission_callback' => function() { return current_user_can('edit_pages'); },
        ],
    ]);
}
add_action('init', 'register_rank_math_meta');

/**
 * Ajoute une option dans le menu "Réglages"
 */
function add_rank_math_api_setting() {
    add_options_page(
        'API Rank Math SEO',
        'API Rank Math SEO',
        'manage_options',
        'rank-math-seo-api-settings',
        'rank_math_api_settings_page'
    );
}
add_action('admin_menu', 'add_rank_math_api_setting');

/**
 * Page de réglages pour activer/désactiver l'extension
 */
function rank_math_api_settings_page() {
    ?>
    <div class="wrap">
        <h1>Paramètres API Rank Math SEO</h1>
        <form method="post" action="options.php">
            <?php
            settings_fields('rank_math_api_settings_group');
            do_settings_sections('rank_math_api_settings_group');
            ?>
            <table class="form-table">
                <tr>
                    <th scope="row">Activer Rank Math SEO dans l'API REST</th>
                    <td>
                        <input type="checkbox" name="enable_rank_math_seo_api" value="1" <?php checked(1, get_option('enable_rank_math_seo_api', 0)); ?>>
                        <p class="description">Cette option permet d'exposer les métadonnées SEO de Rank Math (title et description) dans l'API REST de WordPress.</p>
                    </td>
                </tr>
            </table>
            <?php submit_button(); ?>
        </form>
    </div>
    <?php
}

/**
 * Enregistre l'option
 */
function register_rank_math_api_setting() {
    register_setting('rank_math_api_settings_group', 'enable_rank_math_seo_api');
}
add_action('admin_init', 'register_rank_math_api_setting');

/**
 * Modifie l'API REST pour inclure les métadonnées Rank Math SEO si activé
 */
function expose_rank_math_meta_to_rest($data, $post, $context) {
    // Vérifier si l'option est activée
    $enable_rank_math_seo = get_option('enable_rank_math_seo_api', false);

    if ($enable_rank_math_seo) {
        $data->data['rank_math_title'] = get_post_meta($post->ID, 'rank_math_title', true);
        $data->data['rank_math_description'] = get_post_meta($post->ID, 'rank_math_description', true);
    }

    return $data;
}

// Ajouter le filtre à l'API REST pour les posts
add_filter('rest_prepare_post', 'expose_rank_math_meta_to_rest', 10, 3);

// Ajouter également pour les pages et autres types de contenu personnalisés
add_filter('rest_prepare_page', 'expose_rank_math_meta_to_rest', 10, 3);
