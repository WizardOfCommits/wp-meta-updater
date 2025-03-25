<?php
/**
 * Script de test pour Rank Math SEO API Extension
 * 
 * Ce fichier permet de tester facilement si les métadonnées Rank Math SEO
 * sont correctement exposées dans l'API REST WordPress
 * 
 * Utilisation:
 * 1. Uploadez ce fichier dans le répertoire du plugin
 * 2. Accédez à ce fichier via votre navigateur:
 *    https://votre-site.com/wp-content/plugins/rank-math-seo-api-extension/test-rank-math-api.php?id=123
 *    (remplacez 123 par l'ID d'un article)
 */

// Vérifie si WordPress est chargé, sinon inclut wp-load.php
if (!defined('ABSPATH')) {
    // Chemin relatif vers wp-load.php depuis ce fichier
    $wp_load_path = realpath(dirname(__FILE__) . '/../../../../wp-load.php');
    
    if (file_exists($wp_load_path)) {
        require_once($wp_load_path);
    } else {
        die('WordPress n\'a pas pu être chargé. Vérifiez que ce fichier est bien placé dans le répertoire du plugin.');
    }
}

// Vérifie les permissions d'administrateur
if (!current_user_can('manage_options')) {
    wp_die('Vous n\'avez pas les permissions suffisantes pour accéder à cette page.');
}

// Récupère l'ID du post à tester
$post_id = isset($_GET['id']) ? intval($_GET['id']) : 0;

// Fonction pour faire une requête à l'API REST WordPress
function get_wp_rest_post($post_id) {
    $request = new WP_REST_Request('GET', '/wp/v2/posts/' . $post_id);
    $response = rest_do_request($request);
    
    if ($response->is_error()) {
        return array(
            'error' => true,
            'message' => $response->get_error_message()
        );
    }
    
    return $response->get_data();
}

// Statut actuel de l'option
$option_status = get_option('enable_rank_math_seo_api', false) ? 'activée' : 'désactivée';

// Si un formulaire a été soumis pour basculer l'option
if (isset($_POST['toggle_option'])) {
    $current_value = get_option('enable_rank_math_seo_api', false);
    update_option('enable_rank_math_seo_api', !$current_value);
    $option_status = !$current_value ? 'activée' : 'désactivée';
    echo '<div style="background-color: #dff0d8; color: #3c763d; padding: 10px; margin-bottom: 20px; border-radius: 4px;">
            Option ' . $option_status . ' avec succès!
          </div>';
}

// Titre de la page
$title = 'Test de Rank Math SEO API Extension';
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo $title; ?></title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3 {
            color: #23282d;
        }
        pre {
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
        }
        .status {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 4px;
            font-weight: bold;
        }
        .status-enabled {
            background-color: #dff0d8;
            color: #3c763d;
        }
        .status-disabled {
            background-color: #f2dede;
            color: #a94442;
        }
        .columns {
            display: flex;
            gap: 20px;
        }
        .column {
            flex: 1;
            padding: 15px;
            background-color: #f9f9f9;
            border-radius: 4px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        .meta-title, .meta-desc {
            background-color: #ffffdd;
        }
        .btn {
            display: inline-block;
            padding: 8px 16px;
            background-color: #0073aa;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            border: none;
            cursor: pointer;
        }
        .btn:hover {
            background-color: #005177;
        }
        form {
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <h1><?php echo $title; ?></h1>
    
    <div>
        <h2>Statut actuel de l'option</h2>
        <p>
            L'option "Activer Rank Math SEO dans l'API REST" est actuellement 
            <span class="status <?php echo $option_status === 'activée' ? 'status-enabled' : 'status-disabled'; ?>">
                <?php echo $option_status; ?>
            </span>
        </p>
        
        <form method="post">
            <button type="submit" name="toggle_option" class="btn">
                <?php echo $option_status === 'activée' ? 'Désactiver' : 'Activer'; ?> l'option
            </button>
        </form>
    </div>

    <?php if ($post_id > 0): ?>
        <?php
        // Récupère les données du post via l'API REST WordPress
        $post_data = get_wp_rest_post($post_id);
        
        // Vérifie si des erreurs se sont produites
        if (isset($post_data['error'])) {
            echo '<div style="background-color: #f2dede; color: #a94442; padding: 10px; border-radius: 4px;">
                    Erreur: ' . $post_data['message'] . '
                  </div>';
        } else {
            // Récupère les métadonnées directement de la base de données pour comparaison
            $rank_math_title = get_post_meta($post_id, 'rank_math_title', true);
            $rank_math_description = get_post_meta($post_id, 'rank_math_description', true);
        ?>
            <h2>Résultats du test pour l'article ID: <?php echo $post_id; ?></h2>
            
            <div class="columns">
                <div class="column">
                    <h3>Métadonnées Rank Math SEO (dans la base de données)</h3>
                    <table>
                        <tr>
                            <th>Champ</th>
                            <th>Valeur</th>
                        </tr>
                        <tr class="meta-title">
                            <td>rank_math_title</td>
                            <td><?php echo esc_html($rank_math_title) ?: '<em>Non défini</em>'; ?></td>
                        </tr>
                        <tr class="meta-desc">
                            <td>rank_math_description</td>
                            <td><?php echo esc_html($rank_math_description) ?: '<em>Non défini</em>'; ?></td>
                        </tr>
                    </table>
                </div>
                
                <div class="column">
                    <h3>Réponse de l'API REST WordPress</h3>
                    <table>
                        <tr>
                            <th>Champ</th>
                            <th>Présent dans l'API?</th>
                            <th>Valeur</th>
                        </tr>
                        <tr class="meta-title">
                            <td>rank_math_title</td>
                            <td><?php echo isset($post_data['rank_math_title']) ? 'Oui ✓' : 'Non ✗'; ?></td>
                            <td>
                                <?php 
                                if (isset($post_data['rank_math_title'])) {
                                    echo esc_html($post_data['rank_math_title']);
                                } else {
                                    echo '<em>Non présent dans l\'API</em>';
                                }
                                ?>
                            </td>
                        </tr>
                        <tr class="meta-desc">
                            <td>rank_math_description</td>
                            <td><?php echo isset($post_data['rank_math_description']) ? 'Oui ✓' : 'Non ✗'; ?></td>
                            <td>
                                <?php 
                                if (isset($post_data['rank_math_description'])) {
                                    echo esc_html($post_data['rank_math_description']);
                                } else {
                                    echo '<em>Non présent dans l\'API</em>';
                                }
                                ?>
                            </td>
                        </tr>
                    </table>
                </div>
            </div>
            
            <h3>Réponse JSON complète de l'API REST</h3>
            <pre><?php echo json_encode($post_data, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE); ?></pre>
            
            <?php if ($option_status === 'activée' && (!isset($post_data['rank_math_title']) || !isset($post_data['rank_math_description']))): ?>
                <div style="background-color: #fcf8e3; color: #8a6d3b; padding: 10px; margin-top: 20px; border-radius: 4px;">
                    <strong>Note:</strong> L'option est activée mais les champs Rank Math SEO ne sont pas présents dans la réponse API.
                    Causes possibles:
                    <ul>
                        <li>Les champs Rank Math SEO ne sont pas définis pour cet article</li>
                        <li>Le plugin Rank Math SEO n'est pas installé ou activé</li>
                        <li>Un conflit avec un autre plugin</li>
                    </ul>
                </div>
            <?php endif; ?>
            
            <?php if ($option_status === 'désactivée' && (isset($post_data['rank_math_title']) || isset($post_data['rank_math_description']))): ?>
                <div style="background-color: #fcf8e3; color: #8a6d3b; padding: 10px; margin-top: 20px; border-radius: 4px;">
                    <strong>Attention:</strong> L'option est désactivée mais les champs Rank Math SEO sont présents dans la réponse API.
                    Cela pourrait indiquer qu'un autre plugin ou thème expose également ces métadonnées.
                </div>
            <?php endif; ?>
        <?php
        }
        ?>
    <?php else: ?>
        <div style="background-color: #fcf8e3; color: #8a6d3b; padding: 10px; margin-top: 20px; border-radius: 4px;">
            <p>Aucun ID d'article spécifié. Veuillez ajouter <code>?id=123</code> à l'URL (remplacez 123 par l'ID d'un article).</p>
        </div>
    <?php endif; ?>
    
    <div style="margin-top: 30px;">
        <h2>Instructions</h2>
        <ol>
            <li>Utilisez le bouton ci-dessus pour activer ou désactiver l'option.</li>
            <li>Ajoutez <code>?id=123</code> à l'URL pour spécifier l'ID d'un article à tester (remplacez 123 par l'ID réel).</li>
            <li>Consultez les tableaux pour comparer les métadonnées Rank Math SEO dans la base de données avec celles présentes dans l'API REST.</li>
            <li>Vérifiez que les champs <code>rank_math_title</code> et <code>rank_math_description</code> apparaissent dans l'API seulement quand l'option est activée.</li>
        </ol>
    </div>
</body>
</html>
